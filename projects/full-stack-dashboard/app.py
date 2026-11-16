"""Small full-stack task dashboard with SQLite persistence."""
import sqlite3
from flask import Flask, request, redirect, url_for, render_template_string, jsonify
app=Flask(__name__)
DB="dashboard.db"
HTML="""<!doctype html><title>Project Dashboard</title><h1>Project Dashboard</h1>
<form method=post><input name=title placeholder='Task title' required><button>Add task</button></form>
<ul>{% for t in tasks %}<li>{{t[1]}} — {{t[2]}} <form style='display:inline' method=post action='/done/{{t[0]}}'><button>Toggle</button></form></li>{% endfor %}</ul>"""
def db():
    c=sqlite3.connect(DB); c.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Open')"); return c
@app.get("/")
def home():
    with db() as c: tasks=c.execute("SELECT id,title,status FROM tasks ORDER BY id DESC").fetchall()
    return render_template_string(HTML,tasks=tasks)
@app.post("/")
def add():
    title=request.form.get("title","").strip()
    if title:
        with db() as c: c.execute("INSERT INTO tasks(title) VALUES(?)",(title,))
    return redirect(url_for("home"))
@app.post("/done/<int:task_id>")
def toggle(task_id):
    with db() as c: c.execute("UPDATE tasks SET status=CASE status WHEN 'Open' THEN 'Done' ELSE 'Open' END WHERE id=?",(task_id,))
    return redirect(url_for("home"))
@app.get("/api/tasks")
def api_tasks():
    with db() as c: rows=c.execute("SELECT id,title,status FROM tasks ORDER BY id DESC").fetchall()
    return jsonify([{"id":r[0],"title":r[1],"status":r[2]} for r in rows])
if __name__=="__main__": app.run(debug=False,port=5001)
