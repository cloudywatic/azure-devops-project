import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)


def using_postgres():
    return os.environ.get("DB_HOST") is not None


def get_db_connection():
    if using_postgres():
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD")
        )
        return conn
    else:
        conn = sqlite3.connect("tasks.db")
        return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    if using_postgres():
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(150) NOT NULL
            );
        """)
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            );
        """)

    conn.commit()
    cur.close()
    conn.close()


db_initialized = False


@app.before_request
def setup_database():
    global db_initialized
    if not db_initialized:
        try:
            init_db()
            db_initialized = True
        except Exception as e:
            print(f"Database init failed: {e}")


@app.route("/")
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks;")
        tasks = cur.fetchall()
        cur.close()
        conn.close()

        db_type = "Azure PostgreSQL" if using_postgres() else "Local SQLite"
        return render_template("index.html", tasks=tasks, db_status=f"Connected to {db_type}!")
    except Exception as e:
        return render_template("index.html", tasks=[], db_status=f"Disconnected: {e}")


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")

    if title:
        conn = get_db_connection()
        cur = conn.cursor()

        if using_postgres():
            cur.execute("INSERT INTO tasks (title) VALUES (%s);", (title,))
        else:
            cur.execute("INSERT INTO tasks (title) VALUES (?);", (title,))

        conn.commit()
        cur.close()
        conn.close()

    return redirect(url_for("index"))


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
    try:
        init_db()
    except Exception as e:
        print(f"Could not init DB yet: {e}")

    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)