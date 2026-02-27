import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
from calendar_view import CalendarView
from reminder_manager import ReminderManager
from notifier import start_notifier
from storage import load_reminders
from quotes import get_quote_of_the_day
from mood_tracker import MoodTracker, get_mood
from birthday import BirthdayManager, get_upcoming_birthdays
from countdown import CountdownWidget
from weather_widget import WeatherWidget

THEMES = {
    "dark": {
        "bg": "#2b2b2b",
        "header_bg": "#1e1e1e",
        "search_bg": "#333333",
        "entry_bg": "#1e1e1e",
        "fg": "white",
        "subfg": "#888888",
        "accent": "#4a9eff",
        "footer_bg": "#1e1e1e",
        "footer_fg": "#666666",
        "divider": "#444444",
        "btn_theme_bg": "#444444",
        "listbox_bg": "#1e1e1e",
        "listbox_fg": "white",
        "stats_bg": "#1e1e1e",
        "stats_fg": "#aaaaaa",
        "notes_bg": "#1e1e1e",
        "notes_fg": "white",
        "cal_bg": "#1e1e1e",
        "cal_fg": "white",
        "cal_header_bg": "#333333",
        "cal_header_fg": "#4a9eff",
        "cal_normal_bg": "#2b2b2b",
        "cal_normal_fg": "white",
        "cal_weekend_bg": "#2b2b2b",
        "cal_weekend_fg": "#ff6b6b",
        "cal_other_bg": "#222222",
        "cal_other_fg": "#666666",
        "cal_select_bg": "#4a9eff",
        "cal_select_fg": "white",
        "cal_border": "#444444",
    },
    "light": {
        "bg": "#f0f4f8",
        "header_bg": "#2c3e50",
        "search_bg": "#dde4ed",
        "entry_bg": "#ffffff",
        "fg": "#2c3e50",
        "subfg": "#dde4ed",
        "accent": "#2980b9",
        "footer_bg": "#2c3e50",
        "footer_fg": "#bdc3cb",
        "divider": "#bdc3cb",
        "btn_theme_bg": "#dde4ed",
        "listbox_bg": "#ffffff",
        "listbox_fg": "#2c3e50",
        "stats_bg": "#dde4ed",
        "stats_fg": "#2980b9",
        "notes_bg": "#ffffff",
        "notes_fg": "#2c3e50",
        "cal_bg": "#ffffff",
        "cal_fg": "#2c3e50",
        "cal_header_bg": "#2c3e50",
        "cal_header_fg": "#ffffff",
        "cal_normal_bg": "#f0f4f8",
        "cal_normal_fg": "#2c3e50",
        "cal_weekend_bg": "#f0f4f8",
        "cal_weekend_fg": "#c0392b",
        "cal_other_bg": "#dde4ed",
        "cal_other_fg": "#95a5a6",
        "cal_select_bg": "#2980b9",
        "cal_select_fg": "#ffffff",
        "cal_border": "#bdc3cb",
    }
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📅 Calendar & Reminder App")
        self.geometry("1100x720")
        self.resizable(False, False)
        self.current_theme = "dark"
        self.selected_date = datetime.today().strftime("%Y-%m-%d")
        self._build_ui()
        self.apply_theme()
        self._check_birthdays()
        start_notifier()

    def t(self):
        return THEMES[self.current_theme]

    def _build_ui(self):
        # ── Header ──────────────────────────────────────
        self.header = tk.Frame(self, height=60)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.header_title = tk.Label(
            self.header,
            text="📅 Calendar & Reminder App",
            font=("Helvetica", 17, "bold")
        )
        self.header_title.pack(side="left", padx=20, pady=12)

        self.theme_btn = tk.Button(
            self.header,
            text="☀️ Light Mode",
            command=self.toggle_theme,
            font=("Helvetica", 9, "bold"),
            relief="flat", padx=10, pady=5,
            cursor="hand2"
        )
        self.theme_btn.pack(side="right", padx=10, pady=12)

        tk.Button(
            self.header,
            text="📤 Export CSV",
            command=self.export_csv,
            bg="#1dd1a1", fg="white",
            font=("Helvetica", 9, "bold"),
            relief="flat", padx=10, pady=5,
            cursor="hand2"
        ).pack(side="right", padx=5, pady=12)

        tk.Button(
            self.header,
            text="🎂 Birthdays",
            command=self.open_birthdays,
            bg="#fd79a8", fg="white",
            font=("Helvetica", 9, "bold"),
            relief="flat", padx=10, pady=5,
            cursor="hand2"
        ).pack(side="right", padx=5, pady=12)

        tk.Button(
            self.header,
            text="😊 Mood",
            command=self.open_mood,
            bg="#a29bfe", fg="white",
            font=("Helvetica", 9, "bold"),
            relief="flat", padx=10, pady=5,
            cursor="hand2"
        ).pack(side="right", padx=5, pady=12)

        # ── Quote bar ────────────────────────────────────
        self.quote_frame = tk.Frame(self, height=35)
        self.quote_frame.pack(fill="x")
        self.quote_frame.pack_propagate(False)

        quote, author = get_quote_of_the_day()
        self.quote_lbl = tk.Label(
            self.quote_frame,
            text=f'💬 "{quote}" — {author}',
            font=("Helvetica", 9, "italic"),
            anchor="w"
        )
        self.quote_lbl.pack(side="left", padx=15, pady=8)

        # ── Search bar ───────────────────────────────────
        self.search_frame = tk.Frame(self, height=42)
        self.search_frame.pack(fill="x")
        self.search_frame.pack_propagate(False)

        self.search_lbl = tk.Label(
            self.search_frame,
            text="🔍 Search:",
            font=("Helvetica", 10, "bold")
        )
        self.search_lbl.pack(side="left", padx=15, pady=8)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            width=35,
            font=("Helvetica", 10),
            relief="flat", bd=2
        )
        self.search_entry.pack(side="left", padx=5, pady=8, ipady=3)

        self.search_result_label = tk.Label(
            self.search_frame,
            text="",
            font=("Helvetica", 9, "bold")
        )
        self.search_result_label.pack(side="left", padx=10)

        # ── Main content ─────────────────────────────────
        self.content = tk.Frame(self)
        self.content.pack(fill="both", expand=True, padx=15, pady=8)

        self.cal_view = CalendarView(
            self.content,
            on_date_select=self.on_date_select
        )
        self.cal_view.pack(side="left", fill="both")

        self.divider = tk.Frame(self.content, width=2)
        self.divider.pack(side="left", fill="y", padx=8)

        self.reminder_mgr = ReminderManager(self.content)
        self.reminder_mgr.pack(side="right", fill="both", expand=True)

        # ── Footer ─────────────────────────────────────
        # IMPORTANT: Footer must be created BEFORE anything uses self.footer
        self.footer = tk.Frame(self, height=38)
        self.footer.pack(fill="x", side="bottom")
        self.footer.pack_propagate(False)

        self.footer_lbl = tk.Label(
            self.footer,
            text="🔔 Notifications active  |  📁 Auto-saved",
            font=("Helvetica", 9)
        )
        self.footer_lbl.pack(side="left", padx=15, pady=8)

        self.countdown = CountdownWidget(self.footer, self.t())
        self.countdown.pack(side="left", padx=20)

        self.mood_display = tk.Label(
            self.footer,
            text="",
            font=("Helvetica", 9)
        )
        self.mood_display.pack(side="left", padx=10)

        self.clock_label = tk.Label(
            self.footer,
            text="",
            font=("Helvetica", 9, "bold")
        )
        self.clock_label.pack(side="right", padx=15)

        # Weather widget — after clock, footer already exists
        self.weather_widget = WeatherWidget(self.footer, self.t())
        self.weather_widget.pack(side="right", padx=10)

        self.update_clock()
        self.update_mood_display()

    def update_mood_display(self):
        today = datetime.today().strftime("%Y-%m-%d")
        mood = get_mood(today)
        if mood:
            self.mood_display.config(
                text=f"Today's mood: {mood['emoji']} {mood['label']}"
            )
        else:
            self.mood_display.config(text="")
        self.after(5000, self.update_mood_display)

    def apply_theme(self):
        th = self.t()
        self.configure(bg=th["bg"])

        self.header.configure(bg=th["header_bg"])
        self.header_title.configure(bg=th["header_bg"], fg=th["fg"])
        self.theme_btn.configure(bg=th["btn_theme_bg"], fg=th["fg"])

        self.quote_frame.configure(bg=th["stats_bg"])
        self.quote_lbl.configure(
            bg=th["stats_bg"],
            fg=th["subfg"] if self.current_theme == "dark" else "#555555"
        )

        self.search_frame.configure(bg=th["search_bg"])
        self.search_lbl.configure(bg=th["search_bg"], fg=th["fg"])
        self.search_entry.configure(
            bg=th["entry_bg"], fg=th["fg"],
            insertbackground=th["fg"]
        )
        self.search_result_label.configure(bg=th["search_bg"])

        self.content.configure(bg=th["bg"])
        self.divider.configure(bg=th["divider"])

        self.footer.configure(bg=th["header_bg"])
        self.footer_lbl.configure(bg=th["header_bg"], fg=th["footer_fg"])
        self.clock_label.configure(bg=th["header_bg"], fg=th["accent"])
        self.mood_display.configure(bg=th["header_bg"], fg=th["footer_fg"])

        self.countdown.configure(bg=th["header_bg"])
        self.countdown.title_lbl.configure(bg=th["header_bg"], fg=th["footer_fg"])
        self.countdown.countdown_lbl.configure(bg=th["header_bg"], fg=th["accent"])

        self.weather_widget.configure(bg=th["header_bg"])
        self.weather_widget.weather_lbl.configure(
            bg=th["header_bg"], fg=th["footer_fg"]
        )

        self.cal_view.configure(bg=th["bg"])
        self.cal_view.title_lbl.configure(bg=th["bg"], fg=th["fg"])
        self.cal_view.today_btn.configure(bg=th["accent"], fg="white")
        self.cal_view.cal.configure(
            background=th["cal_bg"],
            foreground=th["cal_fg"],
            selectbackground=th["cal_select_bg"],
            selectforeground=th["cal_select_fg"],
            headersbackground=th["cal_header_bg"],
            headersforeground=th["cal_header_fg"],
            normalbackground=th["cal_normal_bg"],
            normalforeground=th["cal_normal_fg"],
            weekendbackground=th["cal_weekend_bg"],
            weekendforeground=th["cal_weekend_fg"],
            othermonthbackground=th["cal_other_bg"],
            othermonthforeground=th["cal_other_fg"],
            bordercolor=th["cal_border"]
        )

        self.reminder_mgr.configure(bg=th["bg"])
        self.reminder_mgr.title_label.configure(bg=th["bg"], fg=th["fg"])
        self.reminder_mgr.date_label.configure(bg=th["bg"], fg=th["accent"])
        self.reminder_mgr.stats_label.configure(
            bg=th["stats_bg"], fg=th["stats_fg"]
        )
        self.reminder_mgr.listbox.configure(
            bg=th["listbox_bg"], fg=th["listbox_fg"],
            selectbackground=th["accent"]
        )
        self.reminder_mgr.time_entry.configure(
            bg=th["entry_bg"], fg=th["fg"],
            insertbackground=th["fg"]
        )
        self.reminder_mgr.note_entry.configure(
            bg=th["entry_bg"], fg=th["fg"],
            insertbackground=th["fg"]
        )
        self.reminder_mgr.quick_notes.configure(
            bg=th["notes_bg"], fg=th["notes_fg"],
            insertbackground=th["fg"]
        )

        for widget in self.reminder_mgr.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=th["bg"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=th["bg"], fg=th["fg"])
                    if isinstance(child, tk.Radiobutton):
                        child.configure(
                            bg=th["bg"],
                            activebackground=th["bg"],
                            selectcolor=th["entry_bg"]
                        )
            if isinstance(widget, tk.Label):
                widget.configure(bg=th["bg"], fg=th["fg"])

    def toggle_theme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.theme_btn.config(text="🌙 Dark Mode")
        else:
            self.current_theme = "dark"
            self.theme_btn.config(text="☀️ Light Mode")
        self.apply_theme()

    def update_clock(self):
        now = datetime.now().strftime("🕐 %d %b %Y  %H:%M:%S")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)

    def on_date_select(self, date_str):
        self.selected_date = date_str
        self.reminder_mgr.load_date(date_str)
        self.cal_view.refresh_highlights()

    def open_mood(self):
        MoodTracker(self, self.selected_date, self.t(),
                    on_save=self.update_mood_display)

    def open_birthdays(self):
        BirthdayManager(self, self.t())

    def _check_birthdays(self):
        upcoming = get_upcoming_birthdays(days=1)
        for name, date, days_left, age in upcoming:
            if days_left == 0:
                messagebox.showinfo(
                    "🎂 Birthday Today!",
                    f"Today is {name}'s birthday! 🎉\nThey are turning {age}!"
                )

    def on_search(self, *args):
        query = self.search_var.get().strip().lower()
        if not query:
            self.search_result_label.config(text="")
            return
        data = load_reminders()
        count = sum(1 for reminders in data.values()
                    for r in reminders if query in r.lower())
        if count:
            self.search_result_label.config(
                text=f"✅ {count} found", fg="#1dd1a1"
            )
        else:
            self.search_result_label.config(
                text="❌ Not found", fg="#ff6b6b"
            )

    def export_csv(self):
        data = load_reminders()
        if not data:
            messagebox.showinfo("Export", "No reminders to export!")
            return
        filename = "reminders_export.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Reminder"])
            for date, reminders in sorted(data.items()):
                for r in reminders:
                    writer.writerow([date, r])
        messagebox.showinfo(
            "✅ Exported!",
            f"Saved to:\n{os.path.abspath(filename)}"
        )