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
    
    # Track when we last pinged to avoid spamming
    last_ping_time = None
    daily_ping_count = 0
    last_reset_date = datetime.now().date()

    while True:
        try:
            current_time = datetime.now()
            current_date = current_time.date()
            current_hour = current_time.hour
            
            # Reset daily counter at midnight
            if current_date != last_reset_date:
                daily_ping_count = 0
                last_reset_date = current_date
                print(f"🌅 New day! Reset ping counter.")
            
            # Only ping during reasonable hours (9 AM to 9 PM)
            if 9 <= current_hour <= 21:
                base_pings = config.get("max_daily_pings", 3)
                replies_today = get_today_replies()
                max_pings = base_pings + replies_today
                
                # Check if we should ping
                should_ping = False
                
                if daily_ping_count < max_pings:
                    if last_ping_time is None:
                        # First ping of the day
                        should_ping = True
                    else:
                        # Wait at least 2-4 hours between pings
                        min_interval = timedelta(hours=random.randint(2, 4))
                        if current_time - last_ping_time >= min_interval:
                            should_ping = True
                
                if should_ping:
                    print(f"🔮 Triggering Luna ping #{daily_ping_count + 1}")
                    trigger_luna_ping()
                    increment_ping()
                    
                    last_ping_time = current_time
                    daily_ping_count += 1
                    
                    print(f"📊 Today's stats: {daily_ping_count}/{max_pings} pings sent")
            
            # Sleep for 30 minutes before checking again
            time.sleep(1800)  # 30 minutes
            
        except KeyboardInterrupt:
            print("\n🌙 Scheduler stopped by user")
            break
        except Exception as e:
            print(f"⚠️ Scheduler error: {e}")
            time.sleep(300)  # Wait 5 minutes before retrying