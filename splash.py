import tkinter as tk
import time
import threading

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # No window borders

        # Center the splash screen
        w, h = 500, 350
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # Background
        self.canvas = tk.Canvas(
            self.root,
            width=w, height=h,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Gradient-like top bar
        self.canvas.create_rectangle(0, 0, 500, 8, fill="#4a9eff", outline="")

        # App icon & title
        self.canvas.create_text(
            250, 80,
            text="📅",
            font=("Helvetica", 52),
            fill="white"
        )
        self.canvas.create_text(
            250, 150,
            text="Calendar & Reminder App",
            font=("Helvetica", 20, "bold"),
            fill="white"
        )
        self.canvas.create_text(
            250, 185,
            text="Stay organized, never miss a thing!",
            font=("Helvetica", 11),
            fill="#888888"
        )

        # Version
        self.canvas.create_text(
            250, 320,
            text="v2.0  •  Built with Python & Tkinter",
            font=("Helvetica", 9),
            fill="#555555"
        )

        # Progress bar background
        self.canvas.create_rectangle(
            50, 240, 450, 260,
            fill="#333333",
            outline="",
            tags="bar_bg"
        )

        # Progress bar fill
        self.progress_bar = self.canvas.create_rectangle(
            50, 240, 50, 260,
            fill="#4a9eff",
            outline="",
            tags="bar"
        )

        # Loading text
        self.loading_text = self.canvas.create_text(
            250, 275,
            text="Loading...",
            font=("Helvetica", 10),
            fill="#4a9eff"
        )

        # Start progress animation
        self.progress = 0
        self.messages = [
            "Loading calendar...",
            "Setting up reminders...",
            "Preparing notifications...",
            "Loading your data...",
            "Almost ready...✨"
        ]
        self.animate()

    def animate(self):
        steps = 100
        step_width = 400 / steps

        def update(i):
            if i <= steps:
                x2 = 50 + (i * step_width)
                self.canvas.coords(self.progress_bar, 50, 240, x2, 260)

                # Update loading message
                msg_index = min(i // 20, len(self.messages) - 1)
                self.canvas.itemconfig(
                    self.loading_text,
                    text=self.messages[msg_index]
                )
                self.root.update()
                self.root.after(30, lambda: update(i + 1))
            else:
                self.canvas.itemconfig(
                    self.loading_text,
                    text="✅ Ready!",
                    fill="#1dd1a1"
                )
                self.root.update()
                self.root.after(600, self.close)

        update(0)

    def close(self):
        self.root.destroy()