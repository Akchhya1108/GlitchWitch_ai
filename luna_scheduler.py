import time
import random
from datetime import datetime, timedelta
from core.run_luna import trigger_luna_ping
from core.ping_tracker import get_today_replies, increment_ping
from luna_engine import load_config

def run_scheduler():
    config = load_config()
    if not config.get("ping_enabled", True):
        print("🔕 Ping disabled via config.")
        return

    print("🌘 Luna scheduler started...")

    base_pings = config.get("max_daily_pings", 3)
    replies = get_today_replies()
    total_pings = base_pings + replies

    print(f"[Luna] Base: {base_pings}, Replies: {replies} → Total: {total_pings} pings")

    # Spread pings from now to 10 hours ahead
    now = datetime.now()
    end = now + timedelta(hours=10)
    intervals = sorted(random.sample(range(600, int((end - now).total_seconds())), total_pings))

    for i, delay in enumerate(intervals):
        print(f"🔮 Ping #{i+1} scheduled in {delay//60} min")
        time.sleep(delay)  # wait for scheduled time

        trigger_luna_ping()
        increment_ping()
