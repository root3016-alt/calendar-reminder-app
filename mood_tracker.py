import tkinter as tk
from tkinter import scrolledtext
import json
import os
import random
from datetime import datetime
from storage import save_mood_note, get_mood_note

MOOD_FILE = "moods.json"

MOODS = [
    ("😄", "Happy",   "#f9ca24"),
    ("😊", "Good",    "#6ab04c"),
    ("😐", "Neutral", "#95afc0"),
    ("😔", "Sad",     "#778ca3"),
    ("😤", "Stressed","#e55039"),
    ("😴", "Tired",   "#a29bfe"),
    ("🤩", "Excited", "#fd79a8"),
]

MOOD_MESSAGES = {
    "Happy":    ["Amazing! Happiness is contagious — share it with someone today! 💛",
                 "You're glowing today! Keep spreading that joy! 🌟",
                 "Love this energy! A happy you = a better world! 😄"],
    "Good":     ["Great to hear! A good day is a gift 🌈 Make the most of it!",
                 "Steady and strong — that's the way! Keep going! ✅",
                 "Good vibes only! You're on the right track 😊"],
    "Neutral":  ["That's perfectly okay 🌥️ Not every day needs to be extraordinary.",
                 "Neutral days are rest days for the soul — be kind to yourself 🤍",
                 "Sometimes feeling okay is more than enough 😐"],
    "Sad":      ["It's okay to feel sad 💙 Tough times don't last, tough people do.",
                 "Take a deep breath 🌬️ Tomorrow is a brand new day.",
                 "You are stronger than you feel right now 💪 This too shall pass."],
    "Stressed": ["One thing at a time 🧘 You've handled hard days before — you've got this!",
                 "Take 5 minutes to breathe 🌿 A short break can reset everything.",
                 "Stress is temporary, your strength is permanent 💪"],
    "Tired":    ["Rest is productive too 😴 Your body is asking for kindness — listen to it.",
                 "Even the strongest people need rest 🛌 Recharge yourself today.",
                 "It's okay to slow down 💤 You don't have to do everything today."],
    "Excited":  ["Woohoo! 🎉 That energy is amazing — channel it into something great!",
                 "You're on fire today! 🔥 Make the most of this incredible energy!",
                 "Love that excitement! 🚀 Go conquer the world today!"],
}

def load_moods():
    if not os.path.exists(MOOD_FILE):
        return {}
    with open(MOOD_FILE, "r") as f:
        return json.load(f)

def save_mood(date_str, mood_emoji, mood_label):
    data = load_moods()
    data[date_str] = {"emoji": mood_emoji, "label": mood_label}
    with open(MOOD_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_mood(date_str):
    data = load_moods()
    return data.get(date_str, None)


class MoodTracker(tk.Toplevel):
    def __init__(self, parent, date_str, theme, on_save=None):
        super().__init__(parent)
        self.title(f"😊 Mood Tracker — {date_str}")
        self.geometry("460x600")
        self.resizable(False, False)
        self.configure(bg=theme["bg"])
        self.date_str = date_str
        self.on_save = on_save
        self.theme = theme

        # Title
        tk.Label(
            self,
            text="How are you feeling today?",
            font=("Helvetica", 14, "bold"),
            bg=theme["bg"], fg=theme["fg"]
        ).pack(pady=(20, 3))

        tk.Label(
            self,
            text=f"📅 {date_str}",
            font=("Helvetica", 10),
            bg=theme["bg"], fg=theme["accent"]
        ).pack(pady=(0, 12))

        # Mood buttons
        mood_frame = tk.Frame(self, bg=theme["bg"])
        mood_frame.pack(pady=5)

        self.mood_buttons = {}
        for i, (emoji, label, color) in enumerate(MOODS):
            col = i % 4
            row = i // 4
            btn = tk.Button(
                mood_frame,
                text=f"{emoji}\n{label}",
                font=("Helvetica", 10, "bold"),
                bg=theme["entry_bg"], fg=theme["fg"],
                relief="flat", width=7, height=3,
                cursor="hand2",
                command=lambda e=emoji, l=label, c=color: self.select_mood(e, l, c)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.mood_buttons[label] = (btn, color)

        # Mood message
        self.msg_label = tk.Label(
            self,
            text="",
            font=("Helvetica", 10, "italic"),
            bg=theme["bg"], fg="#f9ca24",
            wraplength=400,
            justify="center"
        )
        self.msg_label.pack(pady=(10, 5), padx=20)

        # Divider
        tk.Frame(self, bg=theme["divider"], height=1).pack(
            fill="x", padx=20, pady=8
        )

        # Journal header
        header_frame = tk.Frame(self, bg=theme["bg"])
        header_frame.pack(fill="x", padx=20)

        tk.Label(
            header_frame,
            text="📓 Journal — Write about your day",
            font=("Helvetica", 10, "bold"),
            bg=theme["bg"], fg=theme["fg"]
        ).pack(side="left")

        # Reminder tip
        tip_frame = tk.Frame(self, bg=theme["stats_bg"])
        tip_frame.pack(fill="x", padx=20, pady=(5, 0))

        tk.Label(
            tip_frame,
            text="💡 Tip: Your journal will appear in today's reminder list! Also use ➕ Add button to set timed reminders.",
            font=("Helvetica", 8, "italic"),
            bg=theme["stats_bg"], fg=theme["stats_fg"],
            wraplength=400,
            justify="left"
        ).pack(padx=8, pady=4)

        # Journal text area
        self.journal = scrolledtext.ScrolledText(
            self,
            width=50, height=8,
            bg=theme["entry_bg"], fg=theme["fg"],
            font=("Helvetica", 10),
            relief="flat", wrap="word",
            insertbackground=theme["fg"],
            padx=10, pady=8
        )
        self.journal.pack(padx=20, pady=5)

        # Load existing note or placeholder
        existing_note = get_mood_note(date_str)
        if existing_note:
            self.journal.insert("1.0", existing_note)
        else:
            self.journal.insert("1.0", "Write your thoughts here...")
            self.journal.config(fg="#888888")
            self.journal.bind("<FocusIn>", self._clear_placeholder)

        # Buttons
        btn_frame = tk.Frame(self, bg=theme["bg"])
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="💾 Save Journal",
            command=self.save_journal,
            bg=theme["accent"],
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat", padx=15, pady=6,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="📅 Add Reminder",
            command=self.remind_to_add,
            bg="#ff9f43",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat", padx=15, pady=6,
            cursor="hand2"
        ).pack(side="left", padx=5)

        # Highlight existing mood
        existing = get_mood(date_str)
        if existing:
            for label, (btn, color) in self.mood_buttons.items():
                if label == existing["label"]:
                    btn.configure(bg=color, fg="white")
            self.msg_label.config(
                text=random.choice(
                    MOOD_MESSAGES.get(existing["label"], [""])
                )
            )

        self.status_lbl = tk.Label(
            self, text="",
            font=("Helvetica", 9),
            bg=theme["bg"], fg="#1dd1a1"
        )
        self.status_lbl.pack()

    def _clear_placeholder(self, event):
        if self.journal.get("1.0", "end-1c") == "Write your thoughts here...":
            self.journal.delete("1.0", "end")
            self.journal.config(fg=self.theme["fg"])

    def select_mood(self, emoji, label, color):
        for lbl, (btn, c) in self.mood_buttons.items():
            btn.configure(bg=self.theme["entry_bg"], fg=self.theme["fg"])
        self.mood_buttons[label][0].configure(bg=color, fg="white")
        msg = random.choice(MOOD_MESSAGES.get(label, ["You're doing great! 💙"]))
        self.msg_label.config(text=msg, fg=color)
        save_mood(self.date_str, emoji, label)
        if self.on_save:
            self.on_save()

    def save_journal(self):
        note = self.journal.get("1.0", "end-1c").strip()
        if not note or note == "Write your thoughts here...":
            self.status_lbl.config(
                text="⚠️ Please write something first!",
                fg="#ff6b6b"
            )
            return

        # Save journal AND reflect in reminders list
        save_mood_note(self.date_str, note)

        self.status_lbl.config(
            text="✅ Journal saved & added to today's reminders!",
            fg="#1dd1a1"
        )

        # Refresh reminder panel if open
        if self.on_save:
            self.on_save()

        self.after(1500, self.destroy)

    def remind_to_add(self):
        from tkinter import messagebox
        messagebox.showinfo(
            "📅 Add a Reminder!",
            "Go back to the calendar!\n\nPick any date and use the ➕ Add button to set timed reminders for important events, tasks or goals! 🎯"
        )