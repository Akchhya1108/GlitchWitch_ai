import time
from ui.popup import get_user_input
from core.user_context import get_user_context
from core.mood import get_luna_mood
from core.ping_tracker import increment_reply
from openai_api import get_gpt4o_reply

def handle_chat_loop():
    while True:
        user_input = get_user_input("Luna", "Talk to me:")
        if not user_input:
            break  # User closed or stayed silent

        increment_reply()
        context = get_user_context()
        mood = get_today_mood()
        luna_reply = get_gpt4o_reply(user_input, mood, context)
        response = get_user_input("Luna replies:", luna_reply)

        if not response:
            break  # Stop chatting if user stops responding

        increment_reply()

def chat_with_luna():
    mood = get_luna_mood()
    context = get_user_context()

    while True:
        user_input = get_user_input("🧿 Luna", "Talk to me:")
        if not user_input:
            break

        increment_reply()

        luna_reply = get_gpt4o_reply(user_input + "\nUser context: " + context)
        show_popup(luna_reply)