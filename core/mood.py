from datetime import datetime
from core.journal import get_last_logged_day  # make sure this exists
import random

def get_luna_mood():
    now = datetime.now()
    hour = now.hour
    today = now.strftime("%Y-%m-%d")
    last_logged = get_last_logged_day()

    # Grudge if ghosted
    if last_logged and last_logged != today:
        return "cold" if (now - datetime.strptime(last_logged, "%Y-%m-%d")).days > 1 else "gremlin"

    # Time-based moods
    if 6 <= hour < 12:
        return "affectionate"
    elif 21 <= hour <= 23 or 0 <= hour < 2:
        return "chaotic"

    return random.choice(["affectionate", "cold", "chaotic", "gremlin", "formal"])
