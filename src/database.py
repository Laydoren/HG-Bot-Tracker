from datetime import date
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "infra", "db", "habits.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            target REAL,
            current REAL NOT NULL DEFAULT 0,
            completed INTEGER NOT NULL DEFAULT 0,
            deadline TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def add_habit(user_id, name, frequency):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO habits (user_id, name, frequency, created_at) VALUES (?, ?, ?, ?)""", (user_id, name, frequency, date.today().isoformat()))

    conn.commit()
    conn.close()


def get_habits(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM habits 
        WHERE user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def add_completion(habit_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)""", (habit_id, date.today().isoformat()))

    conn.commit()
    conn.close()


def get_completions(habit_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM completions 
        WHERE habit_id = ?
    """, (habit_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

# Goals

def add_goal(user_id, title, deadline, target=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO goals (user_id, title, target, current, completed, deadline)VALUES (?, ?, ?, 0, 0, ?)""", (user_id, title, target, deadline))

    conn.commit()
    conn.close()

def get_goals(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM goals 
        WHERE user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def update_goal_progress(goal_id, current):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE goals 
        SET current = ? 
        WHERE id = ?
    """, (current, goal_id))

    conn.commit()
    conn.close()

def update_goal_completed(goal_id, completed):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE goals 
        SET completed = ? 
        WHERE id = ?
    """, (int(completed), goal_id))

    conn.commit()
    conn.close()