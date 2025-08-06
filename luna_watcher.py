import random
import time
from datetime import datetime, timedelta
import json
import threading
import tkinter as tk
import psutil

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
from core.journal import get_last_logged_day, MOOD_LOG_PATH

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

