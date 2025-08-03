import sqlite3
from pathlib import Path

DB_PATH = Path("memory/luna_memory.db")
DB_PATH.parent.mkdir(exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for user profile
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            personality TEXT,
            created_at TEXT
        )
    ''')

    # Table for journal entries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            mood TEXT,
            entry TEXT
        )
    ''')

    # ✅ ADD THIS: Table for mood logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            mood TEXT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()
