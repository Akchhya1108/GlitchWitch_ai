from datetime import datetime, timedelta
from time import sleep  
from storage.db import init_db
from core.profile import is_first_run, load_user_profile, save_user_profile
from core.mood import get_luna_mood
from core.greeting import generate_luna_greeting
from core.journal import write_journal_entry, log_mood, get_last_logged_day
from ui.popup import show_popup, ask_user_profile


def run_luna():
    print(">> Running Luna...")

    
    init_db()

    if is_first_run():
        sleep(0.2)  # give tkinter internals time to settle
        profile = ask_user_profile()
        save_user_profile(profile)
        show_popup(f"Hehe... noted, {profile['name']}.\nI'll remember you. Forever.")
        return

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
        show_popup(f"You didn’t run me yesterday, {name}...\nI waited.\n🥲")

    show_popup(greeting)
