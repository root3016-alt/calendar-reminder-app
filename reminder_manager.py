import tkinter as tk
from tkinter import messagebox, ttk
from storage import get_reminders, add_reminder, delete_reminder, load_reminders

PRIORITY_COLORS = {
    "🔴 High":   "#ff6b6b",
    "🟡 Medium": "#ff9f43",
    "🟢 Low":    "#1dd1a1"
}

class ReminderManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2b2b2b")
        self.selected_date = None

        # Title
        self.title_label = tk.Label(
            self,
            text="📝 Reminders",
            font=("Helvetica", 16, "bold"),
            bg="#2b2b2b",
            fg="white"
        )
        self.title_label.pack(pady=(10, 2))

        # Date label
        self.date_label = tk.Label(
            self,
            text="No date selected",
            font=("Helvetica", 11),
            bg="#2b2b2b",
            fg="#4a9eff"
        )
        self.date_label.pack(pady=(0, 5))

        # Stats bar
        self.stats_label = tk.Label(
            self,
            text="📊 Total reminders this month: 0",
            font=("Helvetica", 9),
            bg="#1e1e1e",
            fg="#aaaaaa",
            padx=10,
            pady=4
        )
        self.stats_label.pack(fill="x", padx=10)

        # Listbox frame
        list_frame = tk.Frame(self, bg="#2b2b2b")
        list_frame.pack(padx=10, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            width=38,
            height=8,
            yscrollcommand=scrollbar.set,
            bg="#1e1e1e",
            fg="white",
            selectbackground="#4a9eff",
            selectforeground="white",
            font=("Helvetica", 11),
            relief="flat",
            borderwidth=0
        )
        self.listbox.pack(side="left", fill="both")
        scrollbar.config(command=self.listbox.yview)

        # Priority selector
        priority_frame = tk.Frame(self, bg="#2b2b2b")
        priority_frame.pack(pady=(8, 0))

        tk.Label(
            priority_frame,
            text="Priority:",
            bg="#2b2b2b",
            fg="white",
            font=("Helvetica", 10)
        ).pack(side="left", padx=5)

        self.priority_var = tk.StringVar(value="🟡 Medium")
        for p in PRIORITY_COLORS:
            rb = tk.Radiobutton(
                priority_frame,
                text=p,
                variable=self.priority_var,
                value=p,
                bg="#2b2b2b",
                fg=PRIORITY_COLORS[p],
                selectcolor="#1e1e1e",
                activebackground="#2b2b2b",
                font=("Helvetica", 10, "bold")
            )
            rb.pack(side="left", padx=4)

        # Time entry
        time_frame = tk.Frame(self, bg="#2b2b2b")
        time_frame.pack(pady=(8, 0))

        tk.Label(
            time_frame,
            text="⏰ Time (HH:MM):",
            bg="#2b2b2b",
            fg="white",
            font=("Helvetica", 10)
        ).pack(side="left", padx=5)

        self.time_entry = tk.Entry(
            time_frame,
            width=8,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Helvetica", 11),
            relief="flat"
        )
        self.time_entry.insert(0, "HH:MM")
        self.time_entry.pack(side="left", padx=5)

        # Note entry
        note_frame = tk.Frame(self, bg="#2b2b2b")
        note_frame.pack(pady=5)

        tk.Label(
            note_frame,
            text="📌 Note:",
            bg="#2b2b2b",
            fg="white",
            font=("Helvetica", 10)
        ).pack(side="left", padx=5)

        self.note_entry = tk.Entry(
            note_frame,
            width=28,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Helvetica", 11),
            relief="flat"
        )
        self.note_entry.pack(side="left", padx=5)

        # Buttons
        btn_frame = tk.Frame(self, bg="#2b2b2b")
        btn_frame.pack(pady=8)

        tk.Button(
            btn_frame,
            text="➕ Add",
            command=self.add,
            bg="#4a9eff",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=10, pady=5,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="🗑 Delete",
            command=self.delete,
            bg="#ff6b6b",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=10, pady=5,
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="🔄 Clear All",
            command=self.clear_all,
            bg="#ff9f43",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=10, pady=5,
            cursor="hand2"
        ).pack(side="left", padx=5)

        # Quick notes panel
        tk.Label(
            self,
            text="🗒️ Quick Notes (auto-saved)",
            font=("Helvetica", 10, "bold"),
            bg="#2b2b2b",
            fg="#aaaaaa"
        ).pack(pady=(8, 2))

        self.quick_notes = tk.Text(
            self,
            width=38,
            height=4,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Helvetica", 10),
            relief="flat",
            wrap="word"
        )
        self.quick_notes.pack(padx=10)
        self.quick_notes.bind("<KeyRelease>", self.save_quick_notes)
        self.load_quick_notes()

    def load_date(self, date_str):
        self.selected_date = date_str
        self.date_label.config(text=f"📅 {date_str}")
        self.refresh_list()
        self.update_stats()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        if self.selected_date:
            reminders = get_reminders(self.selected_date)
            if reminders:
                for r in reminders:
                    self.listbox.insert(tk.END, f"  {r}")
                    # Color code by priority
                    idx = self.listbox.size() - 1
                    if "🔴 High" in r:
                        self.listbox.itemconfig(idx, fg="#ff6b6b")
                    elif "🟡 Medium" in r:
                        self.listbox.itemconfig(idx, fg="#ff9f43")
                    elif "🟢 Low" in r:
                        self.listbox.itemconfig(idx, fg="#1dd1a1")
            else:
                self.listbox.insert(tk.END, "  No reminders for this day")

    def update_stats(self):
        if not self.selected_date:
            return
        month = self.selected_date[:7]  # YYYY-MM
        data = load_reminders()
        count = sum(len(v) for k, v in data.items() if k.startswith(month))
        self.stats_label.config(text=f"📊 Total reminders this month: {count}")

    def add(self):
        if not self.selected_date:
            messagebox.showwarning("Warning", "Please select a date first!")
            return
        time_val = self.time_entry.get().strip()
        note_val = self.note_entry.get().strip()
        priority = self.priority_var.get()

        if not note_val:
            messagebox.showwarning("Warning", "Please enter a reminder note!")
            return

        if time_val and time_val != "HH:MM":
            reminder_text = f"{time_val} | {priority} | {note_val}"
        else:
            reminder_text = f"{priority} | {note_val}"

        add_reminder(self.selected_date, reminder_text)
        self.note_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "HH:MM")
        self.refresh_list()
        self.update_stats()

    def delete(self):
        if not self.selected_date:
            return
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reminder to delete!")
            return
        reminder_text = self.listbox.get(selected[0]).strip()
        delete_reminder(self.selected_date, reminder_text)
        self.refresh_list()
        self.update_stats()

    def clear_all(self):
        if not self.selected_date:
            return
        confirm = messagebox.askyesno("Confirm", f"Delete all reminders for {self.selected_date}?")
        if confirm:
            reminders = get_reminders(self.selected_date)
            for r in reminders:
                delete_reminder(self.selected_date, r)
            self.refresh_list()
            self.update_stats()

    def save_quick_notes(self, event=None):
        notes = self.quick_notes.get("1.0", tk.END).strip()
        with open("quick_notes.txt", "w") as f:
            f.write(notes)

    def load_quick_notes(self):
        try:
            with open("quick_notes.txt", "r") as f:
                notes = f.read()
            self.quick_notes.insert("1.0", notes)
        except FileNotFoundError:
            pass