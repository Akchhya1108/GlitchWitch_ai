import time
import random
import psutil
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from storage.db import get_connection
from core.run_luna import trigger_agentic_ping
from core.ping_tracker import increment_ping, get_today_replies
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

class LunaWatcher:
    def __init__(self):
        self.config = load_config()
        self.last_ping_time = None
        self.next_ping_time = None
        self.daily_ping_count = 0
        self.last_reset_date = datetime.now().date()
        self.previous_apps = set()
        self.activity_log = []
        self.schedule_next_ping()
        
    def get_current_apps(self):
        """Get currently running applications"""
        current_apps = set()
        try:
            for proc in psutil.process_iter(['name', 'create_time']):
                try:
                    name = proc.info['name'].lower()
                    # Focus on relevant apps
                    relevant_apps = ['chrome', 'firefox', 'code', 'notepad', 'word', 
                                   'discord', 'spotify', 'steam', 'photoshop', 'figma', 
                                   'notion', 'obsidian', 'teams', 'zoom', 'slack']
                    
                    if any(app in name for app in relevant_apps):
                        current_apps.add(name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error getting apps: {e}")
        
        return current_apps
    
    def detect_activity_changes(self):
        """Detect when user starts/stops important applications"""
        current_apps = self.get_current_apps()
        
        # New apps started
        new_apps = current_apps - self.previous_apps
        # Apps that were closed
        closed_apps = self.previous_apps - current_apps
        
        activity_change = False
        context = ""
        
        if new_apps:
            app_names = ', '.join(new_apps)
            context = f"Started: {app_names}"
            activity_change = True
            print(f"🔍 Luna noticed: {context}")
            
        if closed_apps:
            app_names = ', '.join(closed_apps)
            if context:
                context += f" | Closed: {app_names}"
            else:
                context = f"Closed: {app_names}"
            activity_change = True
            print(f"🔍 Luna noticed: Closed {app_names}")
        
        self.previous_apps = current_apps
        
        # Log activity for context
        if activity_change:
            self.log_activity(context)
            
        return activity_change, context
    
    def log_activity(self, activity):
        """Log user activity for context"""
        timestamp = datetime.now()
        self.activity_log.append({
            'timestamp': timestamp,
            'activity': activity
        })
        
        # Keep only last 10 activities
        if len(self.activity_log) > 10:
            self.activity_log = self.activity_log[-10:]
    
    def get_recent_activity_context(self):
        """Get context from recent activity"""
        if not self.activity_log:
            return "User seems to be idle"
            
        recent = self.activity_log[-3:]  # Last 3 activities
        context_parts = []
        
        for activity in recent:
            time_ago = datetime.now() - activity['timestamp']
            if time_ago.total_seconds() < 3600:  # Within last hour
                mins_ago = int(time_ago.total_seconds() / 60)
                context_parts.append(f"{activity['activity']} ({mins_ago}m ago)")
        
        return " | ".join(context_parts) if context_parts else "Recent activity detected"
    
    def schedule_next_ping(self):
        """Schedule the next ping time"""
        base_pings = self.config.get("max_daily_pings", 3)
        replies_today = get_today_replies()
        max_pings = base_pings + replies_today
        
        if self.daily_ping_count >= max_pings:
            # No more pings today
            tomorrow = datetime.now().replace(hour=9, minute=0, second=0) + timedelta(days=1)
            self.next_ping_time = tomorrow
        else:
            # Schedule next ping in 2-4 hours
            hours_ahead = random.randint(2, 4)
            minutes_ahead = random.randint(0, 59)
            self.next_ping_time = datetime.now() + timedelta(hours=hours_ahead, minutes=minutes_ahead)
        
        print(f"🕒 Next Luna ping scheduled: {self.next_ping_time.strftime('%H:%M')}")
    
    def should_ping_now(self):
        """Check if it's time to ping"""
        current_time = datetime.now()
        current_hour = current_time.hour
        
        # Only ping during reasonable hours
        if not (9 <= current_hour <= 21):
            return False
            
        # Check if it's time
        if self.next_ping_time and current_time >= self.next_ping_time:
            return True
            
        return False
    
    def contextual_ping_trigger(self, activity_context):
        """Sometimes trigger a ping based on activity (10% chance)"""
        if random.random() < 0.1:  # 10% chance
            current_hour = datetime.now().hour
            if 9 <= current_hour <= 21:  # Only during reasonable hours
                print(f"🔮 Luna is curious about your activity: {activity_context}")
                return True
        return False
    
    def trigger_ping_with_context(self, context_reason="scheduled"):
        """Trigger a ping and include activity context"""
        activity_context = self.get_recent_activity_context()
        
        # Store context for the AI to use
        full_context = f"[{context_reason}] Recent activity: {activity_context}"
        
        print(f"🌙 Luna pinging with context: {full_context}")
        trigger_luna_ping(context=full_context)
        increment_ping()
        
        self.last_ping_time = datetime.now()
        self.daily_ping_count += 1
        self.schedule_next_ping()
    
    def print_status(self):
        """Print current Luna status"""
        current_time = datetime.now()
        if self.next_ping_time:
            time_until = self.next_ping_time - current_time
            if time_until.total_seconds() > 0:
                hours = int(time_until.total_seconds() // 3600)
                minutes = int((time_until.total_seconds() % 3600) // 60)
                print(f"⏰ Next Luna ping in: {hours}h {minutes}m")
            else:
                print("⏰ Luna ping due now!")
        
        print(f"📊 Today's pings: {self.daily_ping_count}")
        
        current_apps = self.get_current_apps()
        if current_apps:
            print(f"👁️ Luna sees you using: {', '.join(current_apps)}")
    
    def run(self):
        """Main watcher loop"""
        print("👁️ Luna is now watching in the background...")
        print("Type 'status' to see when Luna will ping next")
        
        while True:
            try:
                current_time = datetime.now()
                current_date = current_time.date()
                
                # Reset daily counter at midnight
                if current_date != self.last_reset_date:
                    self.daily_ping_count = 0
                    self.last_reset_date = current_date
                    self.schedule_next_ping()
                    print(f"🌅 New day! Reset ping counter.")
                
                # Check for activity changes
                activity_changed, activity_context = self.detect_activity_changes()
                
                # Check if scheduled ping time
                if self.should_ping_now():
                    self.trigger_ping_with_context("scheduled")
                
                # Sometimes ping on interesting activity changes
                elif activity_changed and self.contextual_ping_trigger(activity_context):
                    self.trigger_ping_with_context(f"activity: {activity_context}")
                
                # Sleep for 30 seconds between checks
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n🌙 Luna watcher stopped by user")
                break
            except Exception as e:
                print(f"⚠️ Watcher error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def run_interactive_watcher():
    """Run watcher with interactive status commands"""
    watcher = LunaWatcher()
    
    import threading
    import sys
    
    # Start watcher in background thread
    watcher_thread = threading.Thread(target=watcher.run, daemon=True)
    watcher_thread.start()
    
    print("\n🌙 Luna Watcher Commands:")
    print("  'status' - Show next ping time and current activity")
    print("  'ping' - Force Luna to ping now")
    print("  'quit' - Stop Luna watcher")
    print()
    
    while True:
        try:
            command = input("luna> ").lower().strip()
            
            if command == 'status':
                watcher.print_status()
            elif command == 'ping':
                watcher.trigger_ping_with_context("manual")
            elif command in ['quit', 'exit', 'q']:
                print("🌙 Luna going to sleep... Goodbye!")
                sys.exit(0)
            elif command == '':
                continue
            else:
                print("Unknown command. Try 'status', 'ping', or 'quit'")
                
        except KeyboardInterrupt:
            print("\n🌙 Luna going to sleep... Goodbye!")
            sys.exit(0)
        except EOFError:
            sys.exit(0)

if __name__ == "__main__":
    run_interactive_watcher()