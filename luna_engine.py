# luna_engine.py
import openai
import os
import random
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from pathlib import Path

CONFIG_PATH = Path("config.json")

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {
        "use_gpt": True,
        "minimal_mode": False,
        "ping_enabled": True,
        "max_daily_pings": 3
    }

# === ENV SETUP ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === MOOD DEFINITIONS ===
MOODS = ["affectionate", "cold", "gremlin", "trickster"]

# === FILE PATHS ===
MEMORY_DIR = "memory"
USER_PROFILE_PATH = os.path.join(MEMORY_DIR, "user_profile.json")

MOOD_LOG_PATH = Path(os.path.join(MEMORY_DIR, "mood_log.jsonl"))  # Match journal.py

# Ensure memory directory exists
MOOD_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)



