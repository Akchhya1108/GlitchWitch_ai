import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join("memory", "luna_memory.db")

def ensure_ping_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ping_tracker (
            date TEXT PRIMARY KEY,
            pings INTEGER DEFAULT 0,
            replies INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def increment_ping():
    ensure_ping_table()
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ping_tracker (date, pings, replies)
        VALUES (?, 1, 0)
        ON CONFLICT(date) DO UPDATE SET pings = pings + 1
    ''', (today,))
    conn.commit()
    conn.close()

def increment_reply():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ping_tracker (date, pings, replies)
        VALUES (?, 0, 1)
        ON CONFLICT(date) DO UPDATE SET replies = replies + 1
    ''', (today,))
    conn.commit()
    conn.close()

def get_ping_plan():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT replies FROM ping_tracker WHERE date = ?", (today,))
    result = cursor.fetchone()
    conn.close()
    return 2 + (result[0] if result else 0)  # baseline 2 + 1 ping for each reply
