import sqlite3
from datetime import datetime
import os
from storage.db import get_connection
from pathlib import Path

MOOD_LOG_PATH = Path("memory/mood_log.json")  



DB_PATH = os.path.join("memory", "luna_memory.db")

def log_mood(mood, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO mood_logs (timestamp, mood, message) VALUES (?, ?, ?)",
        (timestamp, mood, message)
    )

    conn.commit()
    conn.close()

def write_journal_entry(mood, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO journal (timestamp, mood, entry) VALUES (?, ?, ?)",
        (timestamp, mood, message)
    )

    conn.commit()
    conn.close()

def get_journal_entry(date_str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT mood, entry FROM journal WHERE date = ?", (date_str,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return {"mood": row[0], "entry": row[1]}
    return None

def get_last_logged_day():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(timestamp) FROM journal
    """)

    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        return result[0].split("T")[0]  # Return date portion
    return None