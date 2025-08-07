import random
import sqlite3
from datetime import datetime
from storage.db import get_connection

def get_luna_mood():
    # Later this will depend on mood trends or user interaction
    return random.choice(["affectionate", "cold", "gremlin", "chaotic"])

def log_mood(mood, greeting):
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO mood_log (date, mood, greeting)
        VALUES (?, ?, ?)
    """, (timestamp, mood, greeting))

    conn.commit()
    conn.close()

def get_recent_moods(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, mood, greeting
        FROM mood_log
        ORDER BY date DESC
        LIMIT ?
    """, (limit,))

    moods = cursor.fetchall()
    conn.close()
    
    return moods

def get_today_mood():
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT mood FROM mood_log
        WHERE date LIKE ?
        ORDER BY date DESC
        LIMIT 1
    """, (f"{today}%",))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    else:
        # Fallback if no mood logged today
        return get_luna_mood()

