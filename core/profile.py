import sqlite3
import os

DB_PATH = os.path.join("memory", "luna_memory.db")

def is_first_run():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_profile")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def save_user_profile(profile):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Remove existing entry (assume single user)
    cursor.execute("DELETE FROM user_profile")
    
    cursor.execute('''
        INSERT INTO user_profile (name, age, personality)
        VALUES (?, ?, ?)
    ''', (profile["name"], profile["age"], profile["personality"]))

    conn.commit()
    conn.close()

def load_user_profile():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, age, personality FROM user_profile LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "name": row[0],
            "age": row[1],
            "personality": row[2]
        }
    else:
        return None
