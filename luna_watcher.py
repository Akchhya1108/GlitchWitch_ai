import random
import time
from datetime import datetime, timedelta
import json
import threading
import tkinter as tk

from luna_engine import show_popup, get_luna_mood, generate_luna_greeting, load_user_profile, MOOD_LOG_PATH

# -- check if user interacted today or yesterday --
def interacted_recently():
    if not MOOD_LOG_PATH.exists():
        return False

    with open(MOOD_LOG_PATH, "r") as f:
        logs = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    return today in logs or yesterday in logs

# -- create scheduled popups --
def schedule_random_popups():
    if not interacted_recently():
        return

    times_today = sorted(random.sample(range(9*60, 20*60), k=random.randint(2, 4)))  # Between 9 AM to 8 PM
    print(f"[Watcher] Luna will popup at: {[f'{t//60}:{t%60:02}' for t in times_today]}")

    for t in times_today:
        hour, minute = t // 60, t % 60
        wait_seconds = (datetime(datetime.now().year, datetime.now().month, datetime.now().day, hour, minute) - datetime.now()).total_seconds()
        if wait_seconds > 0:
            threading.Timer(wait_seconds, send_random_popup).start()

def send_random_popup():
    profile = load_user_profile()
    if not profile:
        return
    name = profile.get("name", "User")
    personality = profile.get("personality", "vibes")

    mood = get_luna_mood()
    popup_msg = generate_luna_greeting(mood, name, personality)
    show_popup(popup_msg)

# -- run the watcher --
if __name__ == "__main__":
    schedule_random_popups()
