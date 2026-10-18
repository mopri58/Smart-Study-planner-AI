import sqlite3
import pandas as pd

DB_PATH = "study_planner.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                due_date TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                estimated_hours REAL NOT NULL CHECK (estimated_hours > 0),
                status TEXT NOT NULL DEFAULT 'Pending'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                hours REAL NOT NULL,
                priority REAL NOT NULL,
                reason TEXT NOT NULL
            )
        """)


def add_task(subject, topic, due_date, difficulty, estimated_hours):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO tasks (subject, topic, due_date, difficulty, estimated_hours) VALUES (?, ?, ?, ?, ?)",
            (subject, topic, due_date, difficulty, estimated_hours),
        )


def get_tasks():
    with _connect() as conn:
        return pd.read_sql_query("SELECT * FROM tasks ORDER BY due_date, subject", conn)


def update_task_status(task_id, status):
    if status not in {"Pending", "Completed"}:
        raise ValueError("Status must be Pending or Completed")
    with _connect() as conn:
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))


def delete_task(task_id):
    with _connect() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))


def replace_schedule(schedule_df):
    with _connect() as conn:
        conn.execute("DELETE FROM schedule")
        if schedule_df is not None and not schedule_df.empty:
            schedule_df.to_sql("schedule", conn, if_exists="append", index=False)


def get_schedule():
    with _connect() as conn:
        return pd.read_sql_query("SELECT date, subject, topic, hours, priority, reason FROM schedule ORDER BY date, priority DESC", conn)
