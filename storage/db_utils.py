# storage/db_utils.py

import sqlite3
from datetime import datetime

DB_PATH = "storage/db.py"

def record_interaction(pinged=True, responded=True):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO interactions (timestamp, pinged, responded)
        VALUES (?, ?, ?)
    """, (timestamp, int(pinged), int(responded)))

    conn.commit()
    conn.close()
