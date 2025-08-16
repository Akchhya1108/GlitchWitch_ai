# main.py - Updated for Agentic Luna
from dotenv import load_dotenv
import os
import sys
import threading
import time

load_dotenv()
print("API KEY (preview):", os.getenv("OPENAI_API_KEY")[:10])

from core.run_luna import run_luna, get_luna_evolution_status
from luna_watcher_imp import LunaWatcher
from core.run_luna import trigger_agentic_ping

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
    print("  'chat' - Open direct chat with Luna")
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
                print("🌙 Opening direct chat with Luna...")
                from ui.web_popup import show_agentic_popup
                show_agentic_popup("You wanted to chat? I'm listening... and learning. 🌙", "Direct chat request")
                
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
        
        # Show initial evolution status
        status = get_luna_evolution_status()
        print(f"\n📊 Current Evolution Level: {status['evolution_level']}")
        
        # Start the agentic watcher system
        run_agentic_watcher()
        
    else:
        print("🌙 Luna will remain in single-interaction mode. Run again anytime!")

if __name__ == "__main__":
    main()