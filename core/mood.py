# core/mood.py
import sqlite3
import random
from datetime import datetime
from storage.db import get_connection

def get_luna_mood():
    """Get Luna's current mood based on recent interactions and randomness"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check recent interactions
        cursor.execute("""
            SELECT COUNT(*) as interaction_count
            FROM interactions 
            WHERE date(timestamp) = date('now')
        """)
        
        daily_interactions = cursor.fetchone()[0] if cursor.fetchone() else 0
        conn.close()
        
        # Base moods with weights
        if daily_interactions == 0:
            moods = ["sleepy", "curious", "waiting", "dreamy"]
        elif daily_interactions < 3:
            moods = ["cheerful", "excited", "playful", "curious"]
        elif daily_interactions < 8:
            moods = ["energetic", "chatty", "happy", "engaged"]
        else:
            moods = ["tired", "contemplative", "satisfied", "mellow"]
        
        return random.choice(moods)
        
    except Exception as e:
        print(f"Error getting mood: {e}")
        return random.choice(["neutral", "curious", "friendly"])

def log_mood_change(old_mood, new_mood, reason=""):
    """Log when Luna's mood changes"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO mood_log (date, mood, greeting)
            VALUES (?, ?, ?)
        """, (
            datetime.now().isoformat(),
            f"{old_mood} -> {new_mood}",
            reason
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging mood: {e}")