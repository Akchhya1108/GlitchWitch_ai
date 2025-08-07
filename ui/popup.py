import tkinter as tk
import sys
from core.ping_tracker import increment_reply
from openai_api import get_gpt4o_reply
from core.user_context import get_user_context
from core.mood import get_today_mood

root = None  # Track globally for clean exit

def show_popup(initial_text):
    global root
    root = tk.Tk()
    root.withdraw()

    popup_win = tk.Toplevel(root)
    popup_win.title("Luna")
    popup_win.configure(bg="#ffd6e7")
    popup_win.attributes("-topmost", True)
    popup_win.geometry("+1000+600")
    popup_win.resizable(False, False)

    # Conversation box
    text_area = tk.Text(
        popup_win,
        bg="#ffd6e7",
        fg="#2c2c2c",
        font=("Segoe UI", 11),
        wrap="word",
        height=15,
        width=40,
        bd=0
    )
    text_area.insert(tk.END, f"Luna: {initial_text}\n")
    text_area.config(state=tk.DISABLED)
    text_area.pack(padx=10, pady=10)

    entry = tk.Entry(popup_win, width=40)
    entry.pack(padx=10, pady=(0, 5))

    def append_convo(text):
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, text + "\n")
        text_area.config(state=tk.DISABLED)
        text_area.see(tk.END)

    def send_response():
        user_input = entry.get().strip()
        if not user_input:
            return
        entry.delete(0, tk.END)
        append_convo(f"You: {user_input}")
        try:
            increment_reply()
        except Exception as e:
            print(f"[Tracker error] {e}")
        mood = get_today_mood()
        context = get_user_context()
        prompt = f"[Mood: {mood}] User: {user_input} | Context: {context}"
        try:
            reply = get_gpt4o_reply(prompt)
            append_convo(f"Luna: {reply}")
        except Exception as e:
            append_convo(f"Luna: (⚠️ Luna glitched out: {e})")

    def close_luna():
        try:
            popup_win.destroy()
        except:
            pass
        try:
            if root:
                root.quit()
        except:
            pass
        sys.exit(0)

    send_btn = tk.Button(popup_win, text="Send", command=send_response)
    send_btn.pack(pady=(0, 5))

    close_btn = tk.Button(popup_win, text="❌ Close", command=close_luna)
    close_btn.pack(pady=(0, 10))

    # Handles clicking the "X" in the window titlebar
    popup_win.protocol("WM_DELETE_WINDOW", close_luna)

    root.mainloop()

