import pywinctl
import random

def get_user_context():
    try:
        active_window = pywinctl.getActiveWindow()
        if active_window:
            title = active_window.title
            process = active_window.getProcessName()
            return f"working in '{title}' via {process}"
        else:
            return random.choice([
                "doing mysterious stuff",
                "staring into the void",
                "probably ignoring me again"
            ])
    except Exception as e:
        return f"glitched while watching you: {str(e)}"
