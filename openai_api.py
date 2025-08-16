from openai import OpenAI
from core.mood import get_luna_mood
from luna_engine import load_config
import os

# Load config at module level
config = load_config()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt4o_reply(user_context: str) -> str:
    if not config.get("use_gpt", True) or config.get("minimal_mode", False):
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

# Add a new function for the Instagram UI
def get_openai_response(prompt: str) -> str:
    """Direct OpenAI response for Instagram UI integration"""
    if not config.get("use_gpt", True) or config.get("minimal_mode", False):
        return "I'm in minimal mode right now... my neural networks are taking a break 💤"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Luna, an agentic AI companion who evolves through conversations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚡ My circuits are having trouble connecting... {str(e)[:50]}"