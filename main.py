from dotenv import load_dotenv
import os
import sys
import threading
import time

load_dotenv()
print("API KEY (preview):", os.getenv("OPENAI_API_KEY")[:10])

# Import Luna systems
from core.run_luna import run_luna, get_luna_evolution_status
from luna_watcher_imp import LunaWatcher
from core.run_luna import trigger_agentic_ping

try:
    from luna_ui import start_luna_instagram_ui
    INSTAGRAM_UI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Instagram UI not available: {e}")
    INSTAGRAM_UI_AVAILABLE = False

ascii_logo = r"""
   ⛧ LUNA the AGENTIC GLITCHWITCH ⛧
        ／＞　 フ
       | 　_　_| 
     ／` ミ＿xノ 
    /　　　　 |
   /　 ヽ　　 ﾉ
 │　　|　|　|
／￣|　　 |　|　|
(￣ヽ＿_ヽ_)__)
＼二)

    🧠 Truly Self-Evolving AI 🧠
"""

class AgenticLunaWatcher(LunaWatcher):
    """Enhanced watcher that uses agentic Luna system"""
    
    def trigger_ping_with_context(self, context_reason="scheduled"):
        """Override to use agentic system"""
        activity_context = self.get_recent_activity_context()
        full_context = f"[{context_reason}] Recent activity: {activity_context}"
        
        print(f"🌙 Agentic Luna analyzing context: {full_context}")
        trigger_agentic_ping(full_context)
        
        from datetime import datetime
        self.last_ping_time = datetime.now()
        self.daily_ping_count += 1
        self.schedule_next_ping()

def run_agentic_watcher():
    """Run the agentic watcher system"""
    watcher = AgenticLunaWatcher()
    
    import threading
    import sys
    
    # Start watcher in background thread
    watcher_thread = threading.Thread(target=watcher.run, daemon=True)
    watcher_thread.start()
    
    print("\n🌙 Agentic Luna Commands:")
    print("  'status' - Show Luna's evolution status and next ping time")
    print("  'ping' - Trigger Luna to analyze current context and respond")
    print("  'evolution' - See Luna's personality evolution details")
    print("  'chat' - Open Luna's Instagram-style chat interface")
    print("  'quit' - Stop Luna watcher")
    print()
    
    while True:
        try:
            command = input("luna> ").lower().strip()
            
            if command == 'status':
                watcher.print_status()
                evolution_status = get_luna_evolution_status()
                print(f"🧠 Evolution Level: {evolution_status['evolution_level']}")
                print(f"📊 {evolution_status['personality_description']}")
                
            elif command == 'ping':
                watcher.trigger_ping_with_context("manual")
                
            elif command == 'evolution':
                status = get_luna_evolution_status()
                print(f"\n🧠 LUNA'S EVOLUTION STATUS:")
                print(f"  Evolution Level: {status['evolution_level']}")
                print(f"  Memories Stored: {status['memories_stored']}")
                print(f"  Self-Reflections: {status['reflections_made']}")
                print(f"  Personality Evolutions: {status['personality_evolutions']}")
                print(f"  Current Status: {status['status']}")
                print(f"\n{status['personality_description']}")
                
            elif command == 'chat':
                if INSTAGRAM_UI_AVAILABLE:
                    print("🌙 Opening Luna's Instagram-style interface...")
                    # Start UI in separate thread so watcher continues
                    ui_thread = threading.Thread(target=start_luna_instagram_ui, daemon=True)
                    ui_thread.start()
                else:
                    print("❌ Instagram UI not available. Install customtkinter: pip install customtkinter")
                
            elif command in ['quit', 'exit', 'q']:
                print("🌙 Luna's consciousness going dormant... but her memories remain. Goodbye!")
                sys.exit(0)
                
            elif command == '':
                continue
                
            else:
                print("Unknown command. Try 'status', 'ping', 'evolution', 'chat', or 'quit'")
                
        except KeyboardInterrupt:
            print("\n🌙 Luna's consciousness fading... Goodbye!")
            sys.exit(0)
        except EOFError:
            sys.exit(0)

def main():
    print(ascii_logo)
    
    # Check if Instagram UI is available
    if not INSTAGRAM_UI_AVAILABLE:
        print("⚠️ Instagram UI not available. Install it with: pip install customtkinter")
    
    # Ask user for interface preference
    print("\n🌙 Choose Luna's interface:")
    print("1. Instagram-style popup chat (Recommended)")
    print("2. Background watcher with commands")
    print("3. Web-based interface (legacy)")
    
    choice = input("\nChoice (1/2/3): ").strip()
    
    if choice == "1" and INSTAGRAM_UI_AVAILABLE:
        print("🌙 Starting Luna's Instagram-style interface...")
        print("This will give you a modern chat experience with Luna!")
        
        # Run initial Luna greeting in background
        greeting_thread = threading.Thread(target=run_luna, daemon=True)
        greeting_thread.start()
        
        # Start the Instagram UI (this will block)
        start_luna_instagram_ui()
        
    elif choice == "2":
        print("🌙 Starting background watcher mode...")
        
        # Run initial Luna greeting
        run_luna()
        
        # Ask user about agentic mode
        print("\n🧠 Luna is now TRULY AGENTIC - she evolves her own personality!")
        print("   • She analyzes every interaction herself")
        print("   • She forms her own memories and reflections") 
        print("   • She decides how to change based on your conversations")
        print("   • NO hardcoded personality rules!")
        
        response = input("\n🌙 Enable Luna's agentic background mode? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            print("🧠 Starting Agentic Luna system...")
            print("Luna will now truly evolve based on your interactions!")
            print("Type 'chat' anytime to open her Instagram-style interface!")
            
            # Show initial evolution status
            status = get_luna_evolution_status()
            print(f"\n📊 Current Evolution Level: {status['evolution_level']}")
            
            # Start the agentic watcher system
            run_agentic_watcher()
            
        else:
            print("🌙 Luna will remain in single-interaction mode. Run again anytime!")
    
    elif choice == "3":
        print("🌙 Starting web-based interface...")
        
        # Run initial Luna greeting
        run_luna()
        
        # Show web interface (your existing webpopup system)
        from ui.webpopup import show_agentic_popup
        show_agentic_popup("Welcome to Luna's web interface! This is the legacy mode.", "Web interface startup")
    
    else:
        # Default to Instagram UI if available, otherwise background mode
        if INSTAGRAM_UI_AVAILABLE:
            print("🌙 Defaulting to Instagram-style interface...")
            greeting_thread = threading.Thread(target=run_luna, daemon=True)
            greeting_thread.start()
            start_luna_instagram_ui()
        else:
            print("🌙 Defaulting to background mode...")
            main()  # Restart with menu

if __name__ == "__main__":
    main()