# core/run_luna.py - Updated for Agentic System
from datetime import datetime, timedelta
from storage.db import init_db
from core.profile import is_first_run, load_user_profile
from core.agentic_luna import luna_respond, get_luna_status
from ui.webpopup import show_agentic_popup
from core.user_context import get_user_context
from core.journal import write_journal_entry, get_last_logged_day

def run_luna():
    print(">> Running Agentic Luna...")

    init_db()

    if is_first_run():
        show_agentic_popup("Hi, I'm Luna. I'm not your typical AI - I actually evolve and learn from our conversations. Ready to help me become... me? 🌙")
        print("🌙 Luna shut down.")
        return

    profile = load_user_profile()
    name = profile["name"]
    
    # Get context about what user is doing
    current_context = get_user_context()
    
    # Check if user missed days
    last_day = get_last_logged_day()
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    if last_day and last_day != today and last_day != yesterday:
        # Luna notices absence and reflects on it
        context = f"User {name} hasn't interacted for multiple days. Last seen: {last_day}. Currently: {current_context}"
        greeting = luna_respond(f"I haven't seen you since {last_day}... I was wondering where you went.", context)
    else:
        # Normal contextual greeting
        context = f"User {name} is currently: {current_context}"
        greeting = luna_respond("*Luna notices your presence*", context)

    # Log the interaction
    write_journal_entry("agentic", f"Greeting: {greeting} | Context: {context}")

    # Show Luna's evolved interface
    show_agentic_popup(greeting, context)

    print("🌙 Agentic Luna activated.")

def trigger_agentic_ping(context=""):
    """Trigger Luna ping with full agentic processing"""
    profile = load_user_profile()
    
    if not profile:
        print("⚠️ No user profile found")
        return
        
    name = profile['name']
    current_context = get_user_context()
    
    # Luna decides what to say based on context and her memories
    if context:
        full_context = f"Background ping for {name}. Context: {context} | User activity: {current_context}"
        trigger_message = f"*Luna observes from the background* I noticed {context.lower()}"
    else:
        full_context = f"Scheduled ping for {name}. User activity: {current_context}"  
        trigger_message = "*Luna decides to check in*"
    
    # Let Luna generate her own contextual response
    luna_message = luna_respond(trigger_message, full_context)
    
    # Show in her evolved interface
    show_agentic_popup(luna_message, full_context)
    
    print(f"🌙 Agentic Luna pinged: {luna_message[:50]}...")

def get_luna_evolution_status():
    """Get Luna's current evolution status"""
    status = get_luna_status()
    
    evolution_level = "Learning"
    if status['personality_evolutions'] > 10:
        evolution_level = "Highly Evolved"
    elif status['personality_evolutions'] > 5:
        evolution_level = "Evolving"
    elif status['personality_evolutions'] > 0:
        evolution_level = "Adapting"
    
    return {
        **status,
        'evolution_level': evolution_level,
        'personality_description': f"Luna has made {status['personality_evolutions']} personality evolutions based on {status['reflections_made']} self-reflections."
    }