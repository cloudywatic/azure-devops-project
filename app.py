import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    # Azure will provide these environment variables automatically
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'tasks_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(150) NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM tasks;')
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', tasks=tasks, db_status="Connected to Azure DB!")
    except Exception as e:
        return render_template('index.html', tasks=[], db_status=f"Disconnected: {e}")

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (title) VALUES (%s);', (title,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f"Could not init DB yet: {e}")
    # Azure App Service requires the app to bind to 0.0.0.0
    app.run(host='0.0.0.0', port=8000)