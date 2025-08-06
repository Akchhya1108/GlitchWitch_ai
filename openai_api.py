from openai import OpenAI
from core.mood import get_luna_mood
import os

# Use your API key securely (from .env or os.environ)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt4o_reply(user_context: str) -> str:
    if not config.get("use_gpt", True):
        return "Luna is in minimal mode. No GPT today 💤"
    mood = get_luna_mood()

    prompt = f"""
You are Luna, a glitchy but emotionally aware AI companion. Current mood: {mood}.
User is currently doing: {user_context}.

Respond with a short, moody or playful message. Be unpredictable, maybe ask if they wanna chat, drop a fact, tease them, or just leave a weird but sweet comment.

Keep the reply under 35 words.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Luna, the glitchwitch."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(⚠️ Luna glitched out: {str(e)})"
from luna_engine import load_config
config = load_config()



