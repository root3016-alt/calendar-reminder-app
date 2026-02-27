import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from storage import get_all_dates_with_reminders

class CalendarView(tk.Frame):
    def __init__(self, parent, on_date_select):
        super().__init__(parent, bg="#2b2b2b")
        self.on_date_select = on_date_select

        self.title_lbl = tk.Label(
            self,
            text="📅 Calendar",
            font=("Helvetica", 16, "bold"),
            bg="#2b2b2b",
            fg="white"
        )
        self.title_lbl.pack(pady=(10, 5))

        today = datetime.today()
        self.cal = Calendar(
            self,
            selectmode="day",
            year=today.year,
            month=today.month,
            day=today.day,
            background="#1e1e1e",
            foreground="white",
            selectbackground="#4a9eff",
            selectforeground="white",
            headersbackground="#333333",
            headersforeground="#4a9eff",
            normalbackground="#2b2b2b",
            normalforeground="white",
            weekendbackground="#2b2b2b",
            weekendforeground="#ff6b6b",
            othermonthbackground="#222222",
            othermonthforeground="#666666",
            bordercolor="#444444",
            font=("Helvetica", 11),
            headerfont=("Helvetica", 12, "bold")
        )
        self.cal.pack(padx=10, pady=5)
        self.cal.bind("<<CalendarSelected>>", self._on_date_click)
        self.highlight_reminder_dates()

        self.today_btn = tk.Button(
            self,
            text="Go to Today",
            command=self.go_to_today,
            bg="#4a9eff",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=10, pady=5,
            cursor="hand2"
        )
        self.today_btn.pack(pady=10)

    def _on_date_click(self, event):
        selected = self.cal.get_date()
        date_obj = datetime.strptime(selected, "%m/%d/%y")
        date_str = date_obj.strftime("%Y-%m-%d")
        self.on_date_select(date_str)

    def highlight_reminder_dates(self):
        dates = get_all_dates_with_reminders()
        for date_str in dates:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                self.cal.calevent_create(date_obj, "Reminder", "reminder")
            except Exception:
                pass
        self.cal.tag_config("reminder", background="#ff9f43", foreground="white")

    def refresh_highlights(self):
        self.cal.calevent_remove("all")
        self.highlight_reminder_dates()

    def go_to_today(self):
        today = datetime.today()
        self.cal.selection_set(today)
        date_str = today.strftime("%Y-%m-%d")
        self.on_date_select(date_str)