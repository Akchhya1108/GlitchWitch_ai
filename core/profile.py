from storage.db import get_connection

def is_first_run():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_profile")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def save_user_profile(profile):
    conn = get_connection()
    cursor = conn.cursor()

    # Clear previous profile if any
    cursor.execute("DELETE FROM user_profile")

    cursor.execute("""
        INSERT INTO user_profile (name, age, personality)
        VALUES (?, ?, ?)
    """, (profile["name"], profile["age"], profile["personality"]))

    conn.commit()
    conn.close()

def load_user_profile():
    conn = get_connection()
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
