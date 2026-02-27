import json
import os

FILE = "reminders.json"
MOOD_NOTES_FILE = "mood_notes.json"

def load_reminders():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_reminders(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_reminder(date_str, reminder_text):
    data = load_reminders()
    if date_str not in data:
        data[date_str] = []
    data[date_str].append(reminder_text)
    save_reminders(data)

def delete_reminder(date_str, reminder_text):
    data = load_reminders()
    if date_str in data:
        data[date_str] = [r for r in data[date_str] if r != reminder_text]
        if not data[date_str]:
            del data[date_str]
        save_reminders(data)

def get_reminders(date_str):
    data = load_reminders()
    return data.get(date_str, [])

def get_all_dates_with_reminders():
    data = load_reminders()
    return list(data.keys())

def load_mood_notes():
    if not os.path.exists(MOOD_NOTES_FILE):
        return {}
    with open(MOOD_NOTES_FILE, "r") as f:
        return json.load(f)

def save_mood_note(date_str, note):
    """Save mood journal and also reflect it in reminders."""
    # Save to mood notes file
    data = load_mood_notes()
    data[date_str] = note
    with open(MOOD_NOTES_FILE, "w") as f:
        json.dump(data, f, indent=2)

    # Also reflect in reminders list
    reminders = load_reminders()
    if date_str not in reminders:
        reminders[date_str] = []

    # Remove old journal entry if exists
    reminders[date_str] = [
        r for r in reminders[date_str]
        if not r.startswith("📓 Journal:")
    ]

    # Add new journal entry
    # Truncate long notes for display
    short_note = note[:60] + "..." if len(note) > 60 else note
    reminders[date_str].append(f"📓 Journal: {short_note}")
    save_reminders(reminders)

def get_mood_note(date_str):
    data = load_mood_notes()
    return data.get(date_str, "")