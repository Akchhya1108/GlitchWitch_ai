import os
import json

PROFILE_PATH = "memory/user_profile.json"

def is_first_run():
    return not os.path.exists(PROFILE_PATH)

def load_user_profile():
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)

def save_user_profile(profile):
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=4)
