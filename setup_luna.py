from storage.db import init_db
from core.profile import save_user_profile, is_first_run

def setup_luna():
    print("🌙 Setting up Luna...")
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Check if this is first run
    if is_first_run():
        print("\n👋 Hello! Let's get Luna to know you better...")
        
        name = input("What's your name? ").strip()
        while not name:
            name = input("Please enter your name: ").strip()
            
        age = input("How old are you? (optional, press enter to skip): ").strip()
        age = int(age) if age.isdigit() else None
        
        print("\nWhat kind of personality do you prefer for your AI companion?")
        print("1. Supportive and encouraging")
        print("2. Sarcastic and witty") 
        print("3. Mysterious and cryptic")
        print("4. Let Luna decide")
        
        choice = input("Choose (1-4): ").strip()
        personality_map = {
            "1": "supportive",
            "2": "sarcastic", 
            "3": "mysterious",
            "4": "adaptive"
        }
        personality = personality_map.get(choice, "adaptive")
        
        profile = {
            "name": name,
            "age": age,
            "personality": personality
        }
        
        save_user_profile(profile)
        print(f"✅ Profile saved for {name}")
        
    else:
        print("✅ User profile already exists")
    
    print("\n🌙 Luna is ready! Run 'python main.py' to start.")

if __name__ == "__main__":
    setup_luna()