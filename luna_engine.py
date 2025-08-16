import json
import os

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ config.json not found, using defaults")
        return {
            "use_gpt": True,
            "minimal_mode": False, 
            "ping_enabled": True,
            "max_daily_pings": 3
        }
    except json.JSONDecodeError as e:
        print(f"❌ Error reading config.json: {e}")
        return {
            "use_gpt": True,
            "minimal_mode": False, 
            "ping_enabled": True,
            "max_daily_pings": 3
        }