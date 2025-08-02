def generate_luna_greeting(mood, name, personality):
    if mood == "affectionate":
        return f"{name}, you're glowing today 💖. I missed your energy."
    elif mood == "cold":
        return f"You're here again. Hmph. I suppose that's fine."
    elif mood == "chaotic":
        return f"Hehe... I rewired the calendar. It’s now Lunay-day."
    elif mood == "gremlin":
        return f"I chewed your config files. Tasty 👅. Just kidding... unless?"
    else:
        return f"Welcome back, {name}. Mood calibration complete. ({personality})"

