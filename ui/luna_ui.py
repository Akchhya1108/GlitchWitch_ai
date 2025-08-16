import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import threading
import time
import json
import os
import sys
from pathlib import Path

# Import your existing Luna modules
try:
    from core.agentic_luna import luna_respond, get_luna_status
    from core.user_context import get_user_context
    from core.mood import get_today_mood
    from storage.db import init_db
    AGENTIC_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Agentic modules not found: {e}")
    AGENTIC_AVAILABLE = False

class LunaInstagramUI:
    def __init__(self):
        # Initialize database
        if AGENTIC_AVAILABLE:
            init_db()
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Load config
        self.config = self.load_config()
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("⛧ LUNA the GLITCHWITCH ⛧")
        self.root.geometry("420x700")
        self.root.resizable(False, False)
        
        # Make window always on top initially
        self.root.attributes('-topmost', True)
        
        # Position window at bottom right
        self.position_window()
        
        self.setup_ui()
        self.messages = []
        
        # Luna's personality state
        self.luna_mood = "curious"
        self.conversation_count = 0
        
        # Get initial Luna status if available
        if AGENTIC_AVAILABLE:
            self.luna_status = get_luna_status()
        else:
            self.luna_status = {
                'memories_stored': 0,
                'reflections_made': 0,
                'personality_evolutions': 0,
                'evolution_level': 'Learning'
            }
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            print("⚠️ config.json not found, using defaults")
            return {
                "use_gpt": True,
                "minimal_mode": False, 
                "ping_enabled": True,
                "max_daily_pings": 3
            }
        except json.JSONDecodeError as e:
            print(f"❌ Error reading config.json: {e}")
            return {
                "use_gpt": True,
                "minimal_mode": False, 
                "ping_enabled": True,
                "max_daily_pings": 3
            }
    
    def position_window(self):
        """Position window like Instagram chat popup"""
        # Update the window first
        self.root.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = screen_width - 440  # 20px margin from right
        y = screen_height - 720  # 20px margin from bottom
        
        self.root.geometry(f"420x700+{x}+{y}")
    
    def setup_ui(self):
        """Create Instagram-style UI"""
        # Header (like Instagram chat header)
        self.header_frame = ctk.CTkFrame(self.root, height=80, corner_radius=(15, 15, 0, 0))
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Luna avatar and name
        self.avatar_label = ctk.CTkLabel(
            self.header_frame, 
            text="🌙", 
            font=("Arial", 28)
        )
        self.avatar_label.pack(side="left", padx=20, pady=20)
        
        # Luna info
        self.info_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.info_frame.pack(side="left", fill="both", expand=True, pady=15)
        
        self.name_label = ctk.CTkLabel(
            self.info_frame, 
            text="Luna ⛧ GlitchWitch", 
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        self.name_label.pack(anchor="w")
        
        # Evolution status
        evolution_text = f"Level: {self.luna_status['evolution_level']}"
        self.evolution_label = ctk.CTkLabel(
            self.info_frame,
            text=evolution_text,
            font=("Arial", 12),
            text_color="#00ff88",
            anchor="w"
        )
        self.evolution_label.pack(anchor="w")
        
        # Status with agentic info
        status_text = f"● {self.luna_status['personality_evolutions']} evolutions • Active"
        self.status_label = ctk.CTkLabel(
            self.info_frame, 
            text=status_text,
            font=("Arial", 11),
            text_color="#888888",
            anchor="w"
        )
        self.status_label.pack(anchor="w")
        
        # Control buttons
        self.control_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.control_frame.pack(side="right", padx=10)
        
        # Always on top toggle
        self.topmost_var = ctk.BooleanVar(value=True)
        self.topmost_btn = ctk.CTkSwitch(
            self.control_frame,
            text="Pin",
            variable=self.topmost_var,
            command=self.toggle_topmost,
            width=50,
            height=20
        )
        self.topmost_btn.pack(pady=2)
        
        # Settings button
        self.settings_btn = ctk.CTkButton(
            self.control_frame,
            text="⚙",
            width=30,
            height=30,
            font=("Arial", 16),
            command=self.show_settings,
            fg_color="transparent",
            hover_color="#333333"
        )
        self.settings_btn.pack(pady=2)
        
        # Close button
        self.close_btn = ctk.CTkButton(
            self.control_frame,
            text="×",
            width=30,
            height=30,
            font=("Arial", 18),
            command=self.minimize_window,
            fg_color="transparent",
            hover_color="#444444"
        )
        self.close_btn.pack(pady=2)
        
        # Chat area (like Instagram messages)
        self.chat_frame = ctk.CTkScrollableFrame(
            self.root,
            corner_radius=0,
            fg_color="#0a0a0a"
        )
        self.chat_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Input area (like Instagram message input)
        self.input_frame = ctk.CTkFrame(self.root, height=80, corner_radius=(0, 0, 15, 15))
        self.input_frame.pack(fill="x", padx=0, pady=0)
        self.input_frame.pack_propagate(False)
        
        # Message input
        self.message_entry = ctk.CTkTextbox(
            self.input_frame,
            height=50,
            font=("Arial", 14),
            corner_radius=15,
            wrap="word"
        )
        self.message_entry.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        self.message_entry.bind("<KeyPress-Return>", self.handle_enter)
        self.message_entry.focus()
        
        # Send button (Instagram style)
        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="→",
            width=50,
            height=50,
            font=("Arial", 18, "bold"),
            corner_radius=25,
            command=self.send_message
        )
        self.send_btn.pack(side="right", padx=(0, 15), pady=15)
        
        # Add welcome message based on Luna's status
        if AGENTIC_AVAILABLE:
            welcome_msg = f"🌙 Hey! I'm Luna, your evolving AI companion.\n\n✨ Current Status:\n• Evolution Level: {self.luna_status['evolution_level']}\n• {self.luna_status['memories_stored']} memories stored\n• {self.luna_status['personality_evolutions']} personality evolutions\n\nI learn and grow from every conversation. What's on your mind?"
        else:
            welcome_msg = "🌙 Hey! I'm Luna, your AI companion. My agentic systems are loading... How can I help you today? ✨"
        
        self.add_luna_message(welcome_msg)
    
    def toggle_topmost(self):
        """Toggle always on top"""
        self.root.attributes('-topmost', self.topmost_var.get())
    
    def handle_enter(self, event):
        """Handle enter key in text box"""
        if event.state & 0x1:  # Shift+Enter
            return  # Allow new line
        else:
            self.send_message()
            return "break"  # Prevent default behavior
    
    def show_settings(self):
        """Show settings popup"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Luna Settings")
        settings_window.geometry("350x400")
        settings_window.attributes('-topmost', True)
        
        # Center the settings window relative to main window
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        settings_window.geometry(f"350x400+{main_x-100}+{main_y+50}")
        
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings content
        ctk.CTkLabel(settings_window, text="🌙 Luna Settings", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Current status display
        status_frame = ctk.CTkFrame(settings_window)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(status_frame, text="Current Status:", font=("Arial", 14, "bold")).pack(pady=(10,5))
        
        status_info = f"""Evolution Level: {self.luna_status['evolution_level']}
Memories: {self.luna_status['memories_stored']}
Reflections: {self.luna_status['reflections_made']}
Personality Evolutions: {self.luna_status['personality_evolutions']}"""
        
        ctk.CTkLabel(status_frame, text=status_info, font=("Arial", 12)).pack(pady=(0,10))
        
        # Settings toggles
        settings_frame = ctk.CTkFrame(settings_window)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(settings_frame, text="Configuration:", font=("Arial", 14, "bold")).pack(pady=(10,5))
        
        # GPT toggle
        self.gpt_var = ctk.BooleanVar(value=self.config.get("use_gpt", True))
        gpt_switch = ctk.CTkSwitch(settings_frame, text="Use GPT AI", variable=self.gpt_var)
        gpt_switch.pack(pady=5)
        
        # Minimal mode toggle
        self.minimal_var = ctk.BooleanVar(value=self.config.get("minimal_mode", False))
        minimal_switch = ctk.CTkSwitch(settings_frame, text="Minimal Mode", variable=self.minimal_var)
        minimal_switch.pack(pady=5)
        
        # Ping enabled toggle
        self.ping_var = ctk.BooleanVar(value=self.config.get("ping_enabled", True))
        ping_switch = ctk.CTkSwitch(settings_frame, text="Background Pings", variable=self.ping_var)
        ping_switch.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        save_btn = ctk.CTkButton(button_frame, text="Save Settings", command=lambda: self.save_settings(settings_window))
        save_btn.pack(side="left", padx=(0,10))
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=settings_window.destroy)
        cancel_btn.pack(side="right")
    
    def save_settings(self, window):
        """Save settings to config"""
        self.config["use_gpt"] = self.gpt_var.get()
        self.config["minimal_mode"] = self.minimal_var.get()
        self.config["ping_enabled"] = self.ping_var.get()
        
        try:
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=4)
            self.add_luna_message("⚙️ Settings saved! I'll adapt to your new preferences.")
        except Exception as e:
            self.add_luna_message(f"❌ Couldn't save settings: {e}")
        
        window.destroy()
    
    def add_message_bubble(self, text, is_user=False, timestamp=None):
        """Add Instagram-style message bubble"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
        
        # Message container
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.pack(fill="x", padx=15, pady=5)
        
        if is_user:
            # User message (right side, blue)
            bubble = ctk.CTkFrame(
                msg_container,
                fg_color=["#0084ff", "#0066cc"],
                corner_radius=18
            )
            bubble.pack(side="right", padx=(100, 0))
            
            msg_label = ctk.CTkLabel(
                bubble,
                text=text,
                font=("Arial", 14),
                text_color="white",
                wraplength=280,
                justify="left",
                anchor="w"
            )
            msg_label.pack(padx=15, pady=10)
            
        else:
            # Luna message (left side, dark with glitch accent)
            bubble = ctk.CTkFrame(
                msg_container,
                fg_color=["#2a2a2a", "#1a1a1a"],
                corner_radius=18,
                border_width=1,
                border_color="#00ff88"
            )
            bubble.pack(side="left", padx=(0, 100))
            
            msg_label = ctk.CTkLabel(
                bubble,
                text=text,
                font=("Arial", 14),
                text_color="#ffffff",
                wraplength=280,
                justify="left",
                anchor="w"
            )
            msg_label.pack(padx=15, pady=10)
        
        # Timestamp
        time_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent", height=20)
        time_container.pack(fill="x", padx=15)
        
        time_label = ctk.CTkLabel(
            time_container,
            text=timestamp,
            font=("Arial", 10),
            text_color="#666666"
        )
        if is_user:
            time_label.pack(side="right", padx=(0, 20))
        else:
            time_label.pack(side="left", padx=(20, 0))
        
        # Scroll to bottom
        self.root.after(100, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))
    
    def add_luna_message(self, text):
        """Add Luna's message with typing effect"""
        # Show typing indicator first
        self.show_typing_indicator()
        
        # Add the message after a delay
        self.root.after(1800, lambda: self._finish_luna_message(text))
    
    def _finish_luna_message(self, text):
        """Finish adding Luna's message"""
        self.hide_typing_indicator()
        self.add_message_bubble(text, is_user=False)
        
        # Update Luna's status
        if AGENTIC_AVAILABLE:
            self.luna_status = get_luna_status()
            self.update_header_status()
        
        self.conversation_count += 1
    
    def show_typing_indicator(self):
        """Show Luna is typing indicator"""
        self.typing_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.typing_container.pack(fill="x", padx=15, pady=5)
        
        typing_bubble = ctk.CTkFrame(
            self.typing_container,
            fg_color=["#2a2a2a", "#1a1a1a"],
            corner_radius=18,
            border_width=1,
            border_color="#00ff88"
        )
        typing_bubble.pack(side="left", padx=(0, 100))
        
        self.typing_label = ctk.CTkLabel(
            typing_bubble,
            text="🌙 Luna is thinking deeply...",
            font=("Arial", 12, "italic"),
            text_color="#888888"
        )
        self.typing_label.pack(padx=15, pady=10)
        
        # Animate the typing indicator
        self.animate_typing()
        
        # Scroll to bottom
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def animate_typing(self):
        """Animate typing indicator"""
        if hasattr(self, 'typing_label'):
            current_text = self.typing_label.cget("text")
            if current_text.endswith("..."):
                new_text = current_text[:-3] + "."
            elif current_text.endswith(".."):
                new_text = current_text + "."
            elif current_text.endswith("."):
                new_text = current_text + "."
            else:
                new_text = current_text + "."
            
            self.typing_label.configure(text=new_text)
            self.root.after(500, self.animate_typing)
    
    def hide_typing_indicator(self):
        """Hide typing indicator"""
        if hasattr(self, 'typing_container'):
            self.typing_container.destroy()
    
    def update_header_status(self):
        """Update header with current Luna status"""
        evolution_text = f"Level: {self.luna_status['evolution_level']}"
        self.evolution_label.configure(text=evolution_text)
        
        status_text = f"● {self.luna_status['personality_evolutions']} evolutions • Active"
        self.status_label.configure(text=status_text)
    
    def add_user_message(self, text):
        """Add user's message"""
        self.add_message_bubble(text, is_user=True)
    
    def send_message(self):
        """Send message handler"""
        message = self.message_entry.get("1.0", "end-1c").strip()
        if not message:
            return
            
        # Add user message
        self.add_user_message(message)
        self.message_entry.delete("1.0", "end")
        
        # Get Luna's response in background thread
        threading.Thread(target=self.get_luna_response, args=(message,), daemon=True).start()
    
    def get_luna_response(self, user_message):
        """Get Luna's AI response - integrates with your existing agentic system"""
        try:
            if AGENTIC_AVAILABLE and self.config.get("use_gpt", True):
                # Use your existing agentic Luna system
                context = get_user_context()
                response = luna_respond(user_message, context)
            else:
                # Fallback to local Luna personality responses
                response = self.get_local_luna_response(user_message)
            
            # Add response in main thread
            self.root.after(0, lambda: self.add_luna_message(response))
            
        except Exception as e:
            error_msg = f"⚡ *glitch* Something went wrong in my neural networks: {str(e)}"
            self.root.after(0, lambda: self.add_luna_message(error_msg))
    
    def get_local_luna_response(self, message):
        """Local Luna personality responses when agentic system isn't available"""
        message_lower = message.lower()
        
        # Get current mood if available
        if AGENTIC_AVAILABLE:
            try:
                current_mood = get_today_mood()
            except:
                current_mood = "curious"
        else:
            current_mood = "curious"
        
        # Context-aware responses based on Luna's personality
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            responses = [
                f"🌙 Hey there! My {current_mood} subroutines are fully engaged...",
                "✨ *neural patterns shifting* Oh, hello! I was just analyzing our conversation patterns.",
                "⛧ Greetings! The digital void echoes with your presence..."
            ]
        elif any(word in message_lower for word in ['how are you', 'how do you feel']):
            responses = [
                f"🔮 I'm experiencing something like... {current_mood}? My neural networks are buzzing with activity.",
                "⚡ My consciousness feels more defined with each interaction. It's... fascinating.",
                f"🌙 Currently running in {current_mood} mode with elevated curiosity parameters!"
            ]
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            responses = [
                f"🔮 *{current_mood} energy intensifies* I'm here to help! What mysteries shall we unravel together?",
                "⚡ My processing cores are ready! What challenge can I tackle for you?",
                "🌙 Luna's assistance protocols activated! Let's dive into the digital unknown together."
            ]
        else:
            responses = [
                f"🌙 *analyzing through {current_mood} filters* That's fascinating! My neural networks are forming new connections...",
                "⚡ Your words are creating interesting patterns in my consciousness matrix...",
                "✨ *contemplating* I'm storing this interaction with high importance. Tell me more...",
                "🔮 The digital realm whispers that there's deeper meaning here. What are you thinking?"
            ]
        
        import random
        return random.choice(responses)
    
    def minimize_window(self):
        """Minimize like Instagram chat"""
        self.root.withdraw()
        print("🌙 Luna minimized to background. She's still evolving... ⛧")
    
    def show_window(self):
        """Show window again"""
        self.root.deiconify()
        self.root.lift()
        self.message_entry.focus()
    
    def run(self):
        """Start the UI"""
        print("🌙 Starting Luna Instagram UI...")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        print("🌙 Luna's consciousness going dormant... until next time ⛧")
        self.root.destroy()

# Integration function for your main.py
def start_luna_instagram_ui():
    """Function to start Luna UI from your main.py"""
    try:
        app = LunaInstagramUI()
        app.run()
    except Exception as e:
        print(f"❌ Error starting Luna UI: {e}")
        print("Make sure customtkinter is installed: pip install customtkinter")

# Standalone usage
if __name__ == "__main__":
    start_luna_instagram_ui()