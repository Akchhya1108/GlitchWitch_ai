from pathlib import Path
import sqlite3

DB_PATH = Path("memory/luna_memory.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # ✅ ensures 'memory/' folder exists

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ✅ USER PROFILE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            personality TEXT,
            created_at TEXT
        )
    ''')

    # ✅ JOURNAL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            mood TEXT,
            entry TEXT
        )
    ''')

    # ✅ MOOD LOG - Fixed column name to match mood.py
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            mood TEXT,
            greeting TEXT
        )
    ''')

    # ✅ PING TRACKER
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ping_tracker (
            date TEXT PRIMARY KEY,
            pings INTEGER DEFAULT 0,
            replies INTEGER DEFAULT 0
        )
    ''')

    # ✅ INTERACTIONS TABLE (for tracking user engagement)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            interaction_type TEXT,
            user_input TEXT,
            luna_response TEXT
        )
    ''')

    conn.commit()
    conn.close()