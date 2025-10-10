from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'todos.db'

# Create DB if not exists
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
    )''')
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    todos = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    if task.strip():
        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT INTO todos (task, done) VALUES (?, ?)", (task, False))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/toggle/<int:id>')
def toggle(id):
    conn = sqlite3.connect(DB_NAME)
    todo = conn.execute("SELECT done FROM todos WHERE id = ?", (id,)).fetchone()
    if todo:
        new_status = not todo[0]
        conn.execute("UPDATE todos SET done = ? WHERE id = ?", (new_status, id))
        conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/clear_completed')
def clear_completed():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM todos WHERE done = 1")
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/clear_all')
def clear_all():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM todos")
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

