import threading
import time
import winsound
from datetime import datetime
from plyer import notification
from storage import load_reminders

def play_sound():
    """Play a beep sound on Windows."""
    try:
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    except Exception:
        pass

def check_reminders():
    """Background thread that checks reminders every 60 seconds."""
    while True:
        now = datetime.now()
        date_key = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        reminders = load_reminders()
        for reminder in reminders.get(date_key, []):
            if reminder.startswith(current_time):
                # Play sound
                play_sound()
                # Show notification
                notification.notify(
                    title="🔔 Reminder!",
                    message=reminder,
                    app_name="Calendar & Reminder App",
                    timeout=10
                )
        time.sleep(60)

def start_notifier():
    """Start the background reminder checker thread."""
    t = threading.Thread(target=check_reminders, daemon=True)
    t.start()