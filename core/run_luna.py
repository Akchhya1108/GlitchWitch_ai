from datetime import datetime, timedelta
from storage.db import init_db
from core.profile import is_first_run, load_user_profile
from core.mood import get_luna_mood, get_recent_moods
from core.greeting import generate_luna_greeting
from core.journal import write_journal_entry, log_mood, get_last_logged_day
from ui.popup import show_popup
from core.user_context import get_user_context
from openai_api import get_gpt4o_reply
from core.ping_tracker import ensure_ping_table

def run_luna():
    print(">> Running Luna...")

    init_db()
    ensure_ping_table()

    if is_first_run():
        show_popup("Hii, I'm Luna. You'll get to know me soon enough.")
        print("🌙 Luna shut down.")
        return

    profile = load_user_profile()
    name = profile["name"]
    personality = profile.get("personality", "unknown")

    mood = get_luna_mood()
    greeting = generate_luna_greeting(mood, name, personality)

    # Log journal
    write_journal_entry(mood, greeting)
    log_mood(mood, greeting)

    # Check for missed days
    last_day = get_last_logged_day()
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    if last_day and last_day != today and last_day != yesterday:
        greeting = f"You didn't run me yesterday, {name}...\nI waited.\n🥲"

    # Only show popup ONCE with final greeting
    show_popup(greeting)

    print("🌙 Luna shut down.")

# For scheduled pings (background mode) - now accepts context
def trigger_luna_ping(context=""):
    mood = get_luna_mood()
    profile = load_user_profile()
    
    if not profile:
        print("⚠️ No user profile found")
        return
        
    name = profile['name']
    personality = profile.get('personality', 'unknown')

    # Generate contextual greeting
    if context:
        # Use context to make greeting more relevant
        user_context = f"{get_user_context()} | {context}"
        luna_reply = get_gpt4o_reply(user_context)
    else:
        greeting = generate_luna_greeting(mood, name, personality)
        user_context = get_user_context()
        luna_reply = get_gpt4o_reply(user_context)

    # Log the interaction
    log_mood(mood, luna_reply)
    write_journal_entry(mood, f"Context: {context} | Reply: {luna_reply}")

    show_popup(luna_reply)