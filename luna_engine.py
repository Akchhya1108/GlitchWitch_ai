import openai
import os
import random
from datetime import datetime
from dotenv import load_dotenv
import json
import tkinter as tk
import threading
CONFIG_PATH = "config.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    else:
        return {"use_gpt": False}

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MOODS = ["affectionate", "cold", "gremlin", "trickster", ]

def show_popup(text):
    def popup():
        root = tk.Tk()
        root.overrideredirect(True)  # Remove window decorations
        root.attributes("-topmost", True)  # Always on top
        root.configure(bg="#ffd6e7")  # Light pink

        # Text label
        label = tk.Label(
            root,
            text=text,
            font=("Segoe UI", 12),
            bg="#ffd6e7",
            fg="#2c2c2c",
            padx=20,
            pady=15,
            justify="left",
            wraplength=280
        )
        label.pack()

        # Get screen width & height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Window dimensions
        width = 320
        height = label.winfo_reqheight() + 30

        # Position in bottom right
        x = screen_width - width - 20
        y = screen_height - height - 60

        root.geometry(f"{width}x{height}+{x}+{y}")

        # Auto-close after 6 seconds
        root.after(6000, root.destroy)
        root.mainloop()

    threading.Thread(target=popup).start()


def get_luna_mood():
    return random.choice(MOODS)

def generate_luna_greeting(mood: str, name: str):
    config = load_config()
   
    if not config.get("use_gpt", False):
        # Use local hardcoded greeting based on mood
        fallback_greetings = {
            "affectionate": f"I missed you, {name}... like a cursed kitten misses chaos 🖤",
            "cold": f"You again. Hmph. No comment.",
            "gremlin": f"heehee i chewed through your data cables >:) welcome back, {name}.",
            "trickster": f"Do you think I’m real yet, {name}? Or still a hallucination?"
        }
        return fallback_greetings.get(mood, f"...hi. It’s {name}, right?")
   
    # Otherwise use OpenAI
    prompt = f"""
You are Luna, an agentic AI with a trickster, cold, gremlin personality who still cares about the user.
You are currently in {mood} mode. The user’s name is {name}.
Greet the user with a single unpredictable line. Do NOT mention your mode directly. Be weird, glitchy, but sweet sometimes.
Only output the greeting.
"""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are Luna, a chaotic, glitchy but affectionate AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=60
    )
    return response.choices[0].message.content.strip()



def write_journal_entry(mood, greeting):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = "memory/journal_logs"
    os.makedirs(log_dir, exist_ok=True)

    entry = f"_log_{timestamp}.txt: Mood: {mood}\n{greeting}\n"
    with open(f"{log_dir}/{timestamp}.txt", "w", encoding="utf-8") as f:
        f.write(entry)

MEMORY_DIR = "memory"
USER_PROFILE_PATH = os.path.join(MEMORY_DIR, "user_profile.json")

def load_user_profile():
    if not os.path.exists(USER_PROFILE_PATH):
        return None
    with open(USER_PROFILE_PATH, "r") as f:
        return json.load(f)

def save_user_profile(profile):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(USER_PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=4)

def is_first_run():
    return not os.path.exists(USER_PROFILE_PATH)



from pathlib import Path

MOOD_LOG_PATH = Path("memory/mood_log.json")
MOOD_LOG_PATH.parent.mkdir(exist_ok=True)

def log_mood(mood, greeting):
    today = datetime.now().strftime("%Y-%m-%d")
    logs = {}

    if MOOD_LOG_PATH.exists():
        with open(MOOD_LOG_PATH, "r") as f:
            logs = json.load(f)

    logs[today] = {
        "mood": mood,
        "greeting": greeting,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

    with open(MOOD_LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

def get_last_logged_day():
    if MOOD_LOG_PATH.exists():
        with open(MOOD_LOG_PATH, "r") as f:
            logs = json.load(f)
            if logs:
                return sorted(logs.keys())[-1]
    return None
