import tkinter as tk
import sys
from core.ping_tracker import increment_reply
from openai_api import get_gpt4o_reply
from core.user_context import get_user_context
from core.mood import get_today_mood

root = None

def show_popup(initial_text):
    global root
    root = tk.Tk()
    root.withdraw()

    popup_win = tk.Toplevel(root)
    popup_win.title("Luna")
    popup_win.overrideredirect(True)
    
    # Clean notification size
    popup_width = 300
    popup_height = 100
    
    # Position in bottom-right
    screen_width = popup_win.winfo_screenwidth()
    screen_height = popup_win.winfo_screenheight()
    x = screen_width - popup_width - 20
    y = screen_height - popup_height - 60
    
    popup_win.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    popup_win.configure(bg="#ffffff")  # Clean white background
    popup_win.attributes("-topmost", True)

    # Add subtle shadow effect with border
    shadow_frame = tk.Frame(popup_win, bg="#e0e0e0", bd=1, relief="solid")
    shadow_frame.pack(fill="both", expand=True)

    main_frame = tk.Frame(shadow_frame, bg="#ffffff")
    main_frame.pack(fill="both", expand=True, padx=1, pady=1)

    # Header with app icon and name
    header_frame = tk.Frame(main_frame, bg="#ffffff", height=25)
    header_frame.pack(fill="x", pady=(8,5))
    header_frame.pack_propagate(False)

    # App icon and name
    icon_label = tk.Label(header_frame, text="🌙", bg="#ffffff", fg="#666666", font=("Segoe UI", 10))
    icon_label.pack(side="left", padx=(12,5))
    
    app_name = tk.Label(header_frame, text="LUNA", bg="#ffffff", fg="#666666", font=("Segoe UI", 8, "bold"))
    app_name.pack(side="left")

    # Time stamp
    time_label = tk.Label(header_frame, text="now", bg="#ffffff", fg="#999999", font=("Segoe UI", 8))
    time_label.pack(side="right", padx=(0,12))

    # Message content - simple and clean
    msg_label = tk.Label(
        main_frame, 
        text=initial_text, 
        bg="#ffffff", 
        fg="#333333", 
        font=("Segoe UI", 9),
        wraplength=280,
        justify="left",
        anchor="w"
    )
    msg_label.pack(pady=(0,8), padx=12, fill="x")

    # Simple input field that appears on click
    input_frame = tk.Frame(main_frame, bg="#f5f5f5")
    
    entry = tk.Entry(
        input_frame,
        bg="#ffffff",
        fg="#333333",
        font=("Segoe UI", 9),
        bd=1,
        relief="solid",
        insertbackground="#333333"
    )
    
    reply_label = tk.Label(
        main_frame,
        text="Reply",
        bg="#ffffff",
        fg="#007acc",
        font=("Segoe UI", 8),
        cursor="hand2"
    )
    reply_label.pack(side="bottom", padx=12, pady=(0,8), anchor="w")

    def show_input():
        reply_label.pack_forget()
        input_frame.pack(side="bottom", fill="x", padx=12, pady=(0,8))
        entry.pack(fill="x", ipady=3)
        entry.focus()
        
        # Expand popup slightly
        popup_win.geometry(f"{popup_width}x{popup_height + 30}+{x}+{y-30}")

    def send_response():
        user_input = entry.get().strip()
        if not user_input:
            return
            
        # Show loading
        msg_label.config(text="Luna is typing...")
        popup_win.update()
        
        try:
            increment_reply()
            mood = get_today_mood()
            context = get_user_context()
            prompt = f"[Mood: {mood}] User: {user_input} | Context: {context}"
            reply = get_gpt4o_reply(prompt)
            
            msg_label.config(text=reply)
            input_frame.pack_forget()
            
            # Reset size
            popup_win.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
            
        except Exception as e:
            msg_label.config(text=f"Luna couldn't respond right now")

    def close_notification():
        try:
            popup_win.destroy()
            if root:
                root.quit()
        except:
            pass
        sys.exit(0)

    # Click anywhere to close (like real notifications)
    def on_click(event):
        if event.widget == msg_label or event.widget == main_frame:
            close_notification()

    # Bind events
    reply_label.bind("<Button-1>", lambda e: show_input())
    entry.bind("<Return>", lambda e: send_response())
    msg_label.bind("<Button-1>", on_click)
    main_frame.bind("<Button-1>", on_click)

    # Auto-dismiss after 10 seconds like real notifications
    popup_win.after(10000, close_notification)

    root.mainloop()