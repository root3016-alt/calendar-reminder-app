import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

BIRTHDAY_FILE = "birthdays.json"

def load_birthdays():
    if not os.path.exists(BIRTHDAY_FILE):
        return {}
    with open(BIRTHDAY_FILE, "r") as f:
        return json.load(f)

def save_birthday(name, date_str):
    data = load_birthdays()
    data[name] = date_str
    with open(BIRTHDAY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def delete_birthday(name):
    data = load_birthdays()
    if name in data:
        del data[name]
        with open(BIRTHDAY_FILE, "w") as f:
            json.dump(data, f, indent=2)

def get_upcoming_birthdays(days=30):
    data = load_birthdays()
    today = datetime.today()
    upcoming = []
    for name, date_str in data.items():
        try:
            bday = datetime.strptime(date_str, "%Y-%m-%d")
            this_year = bday.replace(year=today.year)
            if this_year < today:
                this_year = this_year.replace(year=today.year + 1)
            diff = (this_year - today).days
            age = today.year - bday.year
            if this_year.year == today.year + 1:
                age -= 1
            if diff <= days:
                upcoming.append((name, date_str, diff, age + 1))
        except:
            pass
    return sorted(upcoming, key=lambda x: x[2])

class BirthdayManager(tk.Toplevel):
    def __init__(self, parent, theme):
        super().__init__(parent)
        self.title("🎂 Birthday Manager")
        self.geometry("480x500")
        self.resizable(False, False)
        self.configure(bg=theme["bg"])
        self.theme = theme

        tk.Label(
            self,
            text="🎂 Birthday Reminders",
            font=("Helvetica", 16, "bold"),
            bg=theme["bg"],
            fg=theme["fg"]
        ).pack(pady=(20, 5))

        # Upcoming birthdays
        tk.Label(
            self,
            text="🔔 Upcoming in next 30 days:",
            font=("Helvetica", 11, "bold"),
            bg=theme["bg"],
            fg=theme["accent"]
        ).pack(pady=(10, 5))

        self.upcoming_frame = tk.Frame(self, bg=theme["bg"])
        self.upcoming_frame.pack(fill="x", padx=20)
        self.refresh_upcoming()

        # Divider
        tk.Frame(self, bg=theme["divider"], height=1).pack(
            fill="x", padx=20, pady=10
        )

        # Add birthday
        tk.Label(
            self,
            text="➕ Add New Birthday",
            font=("Helvetica", 11, "bold"),
            bg=theme["bg"],
            fg=theme["fg"]
        ).pack()

        form = tk.Frame(self, bg=theme["bg"])
        form.pack(pady=10)

        tk.Label(form, text="Name:", bg=theme["bg"],
                 fg=theme["fg"], font=("Helvetica", 10)).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.name_entry = tk.Entry(
            form, width=20, bg=theme["entry_bg"],
            fg=theme["fg"], insertbackground=theme["fg"],
            font=("Helvetica", 10), relief="flat"
        )
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Date\n(YYYY-MM-DD):", bg=theme["bg"],
                 fg=theme["fg"], font=("Helvetica", 10)).grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.date_entry = tk.Entry(
            form, width=20, bg=theme["entry_bg"],
            fg=theme["fg"], insertbackground=theme["fg"],
            font=("Helvetica", 10), relief="flat"
        )
        self.date_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(
            self,
            text="🎂 Save Birthday",
            command=self.add_birthday,
            bg=theme["accent"],
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=15, pady=6,
            cursor="hand2"
        ).pack(pady=5)

        # All birthdays list
        tk.Label(
            self,
            text="📋 All Birthdays:",
            font=("Helvetica", 11, "bold"),
            bg=theme["bg"],
            fg=theme["fg"]
        ).pack(pady=(10, 2))

        self.list_frame = tk.Frame(self, bg=theme["bg"])
        self.list_frame.pack(fill="x", padx=20)
        self.refresh_list()

    def refresh_upcoming(self):
        for w in self.upcoming_frame.winfo_children():
            w.destroy()
        upcoming = get_upcoming_birthdays()
        if not upcoming:
            tk.Label(
                self.upcoming_frame,
                text="No upcoming birthdays in next 30 days",
                font=("Helvetica", 9),
                bg=self.theme["bg"],
                fg=self.theme["subfg"]
            ).pack()
        else:
            for name, date, days_left, age in upcoming:
                text = f"🎂 {name} — {date}  |  {'Today! 🎉' if days_left == 0 else f'In {days_left} days'} (Turns {age})"
                color = "#f9ca24" if days_left == 0 else self.theme["fg"]
                tk.Label(
                    self.upcoming_frame,
                    text=text,
                    font=("Helvetica", 9),
                    bg=self.theme["bg"],
                    fg=color
                ).pack(anchor="w", pady=1)

    def refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        data = load_birthdays()
        if not data:
            tk.Label(
                self.list_frame,
                text="No birthdays saved yet",
                font=("Helvetica", 9),
                bg=self.theme["bg"],
                fg=self.theme["subfg"]
            ).pack()
        else:
            for name, date in data.items():
                row = tk.Frame(self.list_frame, bg=self.theme["bg"])
                row.pack(fill="x", pady=1)
                tk.Label(
                    row,
                    text=f"🎂 {name} — {date}",
                    font=("Helvetica", 9),
                    bg=self.theme["bg"],
                    fg=self.theme["fg"]
                ).pack(side="left")
                tk.Button(
                    row,
                    text="🗑",
                    command=lambda n=name: self.delete(n),
                    bg=self.theme["bg"],
                    fg="#ff6b6b",
                    font=("Helvetica", 9),
                    relief="flat",
                    cursor="hand2"
                ).pack(side="right")

    def add_birthday(self):
        name = self.name_entry.get().strip()
        date = self.date_entry.get().strip()
        if not name or not date:
            messagebox.showwarning("Warning", "Please fill in both fields!")
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format!")
            return
        save_birthday(name, date)
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.refresh_upcoming()
        self.refresh_list()
        messagebox.showinfo("Success", f"🎂 {name}'s birthday saved!")

    def delete(self, name):
        if messagebox.askyesno("Confirm", f"Delete {name}'s birthday?"):
            delete_birthday(name)
            self.refresh_upcoming()
            self.refresh_list()