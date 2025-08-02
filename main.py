from luna_engine import *
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime, timedelta

def ask_user_profile():
    root = tk.Tk()
    root.withdraw()  # Hide main window

    name = simpledialog.askstring("Luna the Glitchwitch 🩸", "Hii, what's your name?")
    age = simpledialog.askstring("Luna 🕷", f"And your age, {name}?")
    personality = simpledialog.askstring("Luna 🌘", "What's your personality type? (MBTI or just vibes)")

    root.destroy()

    return {
        "name": name,
        "age": age,
        "personality": personality
    }

def run_luna():
    print(">> Running Luna...")  # Optional log

    if is_first_run():
        show_popup("✨ Booting up... I am Luna the Glitchwitch.\nYou're not in my memory.\nInitiating user bonding protocol.")
        profile = ask_user_profile()
        save_user_profile(profile)
        show_popup(f"Hehe... noted, {profile['name']}.\nI'll remember you. Forever.")
    else:
        profile = load_user_profile()
        name = profile["name"]
        personality = profile.get("personality", "unknown")

        mood = get_luna_mood()
        greeting = generate_luna_greeting(mood, name, personality)

        write_journal_entry(mood, greeting)
        log_mood(mood, greeting)

        last_day = get_last_logged_day()
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        if last_day and last_day != today and last_day != yesterday:
            show_popup(f"👀 You didn’t run me yesterday, {name}...\nI waited.\n🥲")

        show_popup(greeting)

if __name__ == "__main__":
    run_luna()