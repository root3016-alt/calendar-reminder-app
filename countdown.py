import tkinter as tk
from datetime import datetime
from storage import load_reminders

def get_next_reminder():
    """Find the next upcoming reminder."""
    now = datetime.now()
    data = load_reminders()
    upcoming = []

    for date_str, reminders in data.items():
        for reminder in reminders:
            try:
                parts = reminder.split("|")
                if len(parts) >= 1:
                    time_part = parts[0].strip()
                    if ":" in time_part and len(time_part) == 5:
                        dt_str = f"{date_str} {time_part}"
                        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                        if dt > now:
                            upcoming.append((dt, reminder.strip()))
            except:
                pass

    if upcoming:
        upcoming.sort(key=lambda x: x[0])
        return upcoming[0]
    return None

class CountdownWidget(tk.Frame):
    def __init__(self, parent, theme):
        super().__init__(parent, bg=theme["bg"])
        self.theme = theme

        self.title_lbl = tk.Label(
            self,
            text="⏳ Next Reminder",
            font=("Helvetica", 10, "bold"),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        self.title_lbl.pack()

        self.countdown_lbl = tk.Label(
            self,
            text="No upcoming reminders",
            font=("Helvetica", 9),
            bg=theme["bg"],
            fg=theme["accent"]
        )
        self.countdown_lbl.pack()
        self.tick()

    def tick(self):
        result = get_next_reminder()
        if result:
            dt, reminder = result
            now = datetime.now()
            diff = dt - now
            total_seconds = int(diff.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            label = reminder[:25] + "..." if len(reminder) > 25 else reminder
            self.countdown_lbl.config(
                text=f"{label}\n⏱ {hours:02d}h {minutes:02d}m {seconds:02d}s"
            )
        else:
            self.countdown_lbl.config(text="No upcoming reminders")
        self.after(1000, self.tick)