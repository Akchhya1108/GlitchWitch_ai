from dotenv import load_dotenv
import os
import sys
import threading
import time

load_dotenv()
print("API KEY (preview):", os.getenv("OPENAI_API_KEY")[:10])

from core.run_luna import run_luna
from luna_watcher_imp import run_interactive_watcher

ascii_logo = r"""
   ⛧ LUNA the GLITCHWITCH ⛧
        ／＞　 フ
       | 　_　_| 
     ／` ミ＿xノ 
    /　　　　 |
   /　 ヽ　　 ﾉ
 │　　|　|　|
／￣|　　 |　|　|
(￣ヽ＿_ヽ_)__)
＼二)
"""

def main():
    print(ascii_logo)
    
    # Run initial Luna greeting
    run_luna()
    
    # Ask user if they want to enable background pings
    response = input("\n🌙 Enable Luna's background pings throughout the day? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("🌘 Starting Luna watcher...")
        print("Luna will now monitor your activity and ping contextually!")
        
        # Start the improved watcher system
        run_interactive_watcher()
    else:
        print("🌙 Luna will only run when called. Goodbye!")

if __name__ == "__main__":
    main()