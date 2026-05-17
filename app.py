import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2

app = Flask(__name__)


def using_postgres():
    return os.environ.get("DB_HOST") is not None


def get_db_connection():
    if using_postgres():
        return psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD")
        )
    return sqlite3.connect("tasks.db")


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    if using_postgres():
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(150) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'in_progress'
            );
        """)
        cur.execute("""
            ALTER TABLE tasks
            ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'in_progress';
        """)
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'in_progress'
            );
        """)

        cur.execute("PRAGMA table_info(tasks);")
        columns = [column[1] for column in cur.fetchall()]
        if "status" not in columns:
            cur.execute("ALTER TABLE tasks ADD COLUMN status TEXT NOT NULL DEFAULT 'in_progress';")

    conn.commit()
    cur.close()
    conn.close()


db_initialized = False


@app.before_request
def setup_database():
    global db_initialized
    if not db_initialized:
        init_db()
        db_initialized = True


@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, status FROM tasks ORDER BY id DESC;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()

    in_progress = [task for task in tasks if task[2] == "in_progress"]
    done = [task for task in tasks if task[2] == "done"]

    db_type = "Azure PostgreSQL" if using_postgres() else "Local SQLite"
    return render_template(
        "index.html",
        in_progress=in_progress,
        done=done,
        db_status=f"Connected to {db_type}"
    )


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")

    if title:
        conn = get_db_connection()
        cur = conn.cursor()

        if using_postgres():
            cur.execute("INSERT INTO tasks (title, status) VALUES (%s, %s);", (title, "in_progress"))
        else:
            cur.execute("INSERT INTO tasks (title, status) VALUES (?, ?);", (title, "in_progress"))

        conn.commit()
        cur.close()
        conn.close()

    return redirect(url_for("index"))


@app.route("/update-status", methods=["POST"])
def update_status():
    data = request.get_json()
    task_id = data.get("id")
    status = data.get("status")

    if status not in ["in_progress", "done"]:
        return jsonify({"success": False, "error": "Invalid status"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    if using_postgres():
        cur.execute("UPDATE tasks SET status = %s WHERE id = %s;", (status, task_id))
    else:
        cur.execute("UPDATE tasks SET status = ? WHERE id = ?;", (status, task_id))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"success": True})


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if using_postgres():
        cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    else:
        cur.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)