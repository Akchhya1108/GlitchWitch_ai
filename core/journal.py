from datetime import datetime
import os

MOOD_LOG_PATH = "memory/mood_log.jsonl"

def log_mood(mood, greeting):
    os.makedirs(os.path.dirname(MOOD_LOG_PATH), exist_ok=True)
    with open(MOOD_LOG_PATH, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {mood} | {greeting}\n")

def write_journal_entry(mood, greeting):
    day = datetime.now().strftime("%Y-%m-%d")
    path = f"memory/journal/{day}.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(f"🩸 {day} [{mood}]\n\n{greeting}\n")
        
def get_last_logged_day():
    if not os.path.exists(MOOD_LOG_PATH):
        return None
    with open(MOOD_LOG_PATH, "r") as f:
        lines = f.readlines()
        if not lines:
            return None
        last_entry = lines[-1].split("|")[0].strip()
        return last_entry[:10]  # yyyy-mm-dd
