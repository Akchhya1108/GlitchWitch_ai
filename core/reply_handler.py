from ui.popup import show_popup
from core.user_context import get_user_context
from core.mood import get_today_mood
from core.ping_tracker import increment_reply
from openai_api import get_gpt4o_reply

def chat_with_luna():
    mood = get_today_mood()
    context = get_user_context()

    # Initial message
    initial_message = "You're here again. Hmph. I suppose that's fine."
    show_popup(initial_message)  # Only pass one arg (updated to match your current popup.py)
