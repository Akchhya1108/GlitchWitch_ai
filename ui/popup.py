import tkinter as tk
from tkinter import simpledialog, messagebox
import threading

def show_popup(text):
    def popup():
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        popup_win = tk.Toplevel(root)
        popup_win.overrideredirect(True)
        popup_win.attributes("-topmost", True)
        popup_win.configure(bg="#ffd6e7")

        label = tk.Label(
            popup_win,
            text=text,
            font=("Segoe UI", 12),
            bg="#ffd6e7",
            fg="#2c2c2c",
            padx=20,
            pady=15,
            justify="left",
            wraplength=280
        )
        label.pack()

        popup_win.update_idletasks()
        width = 320
        height = popup_win.winfo_reqheight() + 30
        screen_width = popup_win.winfo_screenwidth()
        screen_height = popup_win.winfo_screenheight()
        x = screen_width - width - 20
        y = screen_height - height - 60

        popup_win.geometry(f"{width}x{height}+{x}+{y}")

        root.after(6000, root.destroy)
        root.mainloop()

    threading.Thread(target=popup).start()


def ask_user_profile():
    root = tk.Tk()
    root.withdraw()
    name = simpledialog.askstring("Luna the Glitchwitch 🩸", "Hii, what's your name?")
    age = simpledialog.askstring("Luna 🕷", f"And your age, {name}?")
    personality = simpledialog.askstring("Luna 🌘", "What's your personality type? (MBTI or just vibes)")
    root.destroy()
    return {
        "name": name,
        "age": age,
        "personality": personality
    }
def get_user_response(timeout=60):
    root = tk.Tk()
    root.withdraw()
    root.after(timeout * 1000, root.quit)  # timeout in ms

    try:
        return simpledialog.askstring("Luna wants to talk", "Reply to Luna (or wait to ignore):")
    except Exception:
        return None
