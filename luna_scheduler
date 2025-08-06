import time
import random
from core.run_luna import trigger_luna_ping
from core.ping_tracker import get_today_multiplier

def run_scheduler():
    print("🌘 Luna scheduler started...")

    while True:
        multiplier = get_today_multiplier()
        wait_time = random.randint(7200, 14400) // multiplier
        print(f"🔮 Next Luna ping in {wait_time // 60} minutes...")
        time.sleep(wait_time)

        trigger_luna_ping()

if __name__ == "__main__":
    run_scheduler()