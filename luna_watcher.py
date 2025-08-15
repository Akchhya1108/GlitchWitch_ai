import random
import sqlite3
from storage.db import DB_PATH
import time
from datetime import datetime, timedelta
import json
import threading
import tkinter as tk
import psutil
from db.interactions import record_interaction


def get_user_context():
    """Returns basic context about what apps/processes the user is currently running."""
    context = []
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name']
            if name:
                context.append(name.lower())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_apps = [app for app in context if any(x in app for x in ['chrome', 'code', 'word', 'notion', 'discord', 'spotify'])]
    if not top_apps:
        return "Just vibing. No major apps running."
    return f"User is running: {', '.join(set(top_apps))}"

from ui.popup import show_popup
from core.mood import get_luna_mood
from core.greeting import generate_luna_greeting
from core.profile import load_user_profile
from core.journal import get_last_logged_day

# -- check if user interacted today or yesterday --
def interacted_recently():
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM interactions
        WHERE DATE(timestamp) IN (?, ?)
    """, (today, yesterday))

    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


# -- create scheduled popups --
import random
from datetime import datetime, timedelta
import schedule
import time

def schedule_random_popups():
    if not interacted_recently():
        print("No recent interaction. Luna won’t schedule future pings today, but this one is for fun.")
        return

    now = datetime.now()
    min_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    max_time = now.replace(hour=20, minute=0, second=0, microsecond=0)

    if now > max_time:
        print("Too late in the day to schedule popups.")
        return

    # Pick 2 to 4 random times
    num_pings = random.randint(2, 4)
    scheduled_times = []

    for _ in range(num_pings):
        random_minutes = random.randint(0, int((max_time - now).total_seconds() // 60))
        ping_time = now + timedelta(minutes=random_minutes)
        scheduled_times.append(ping_time)

        # Schedule each ping
        schedule_time_str = ping_time.strftime("%H:%M")
        schedule.every().day.at(schedule_time_str).do(trigger_luna_ping)

    print("[Debug] Scheduled ping times:")
    for job in schedule.jobs:
        print(" -", job.at_time)


    # Start the scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(1)



def send_random_popup():
    profile = load_user_profile()
    if not profile:
        return
    name = profile.get("name", "User")
    personality = profile.get("personality", "vibes")

    mood = get_luna_mood()
    popup_msg = generate_luna_greeting(mood, name, personality)
    show_popup(popup_msg)
    print("[Watcher] Luna is sending a popup at", datetime.now().strftime("%H:%M"))

    

def get_user_context():
    """Returns basic context about what apps/processes the user is currently running."""
    context = []
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name']
            if name:
                context.append(name.lower())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_apps = [app for app in context if any(x in app for x in ['chrome', 'code', 'word', 'notion', 'discord', 'spotify'])]
    if not top_apps:
        return "Just vibing. No major apps running."
    return f"User is running: {', '.join(set(top_apps))}"


# -- run the watcher --
if __name__ == "__main__":
    schedule_random_popups()

send_random_popup()
