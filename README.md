# 📅 Calendar & Reminder App

> A beautiful, full-featured calendar and reminder web app built with Python & Streamlit. Works on any device — phone, tablet, or laptop!

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)

---

## 🌐 Live Demo

### 👉 [https://rcdwx5zu4scbvffx4.streamlit.app](https://rcdwx5zu4scbvffx4.streamlit.app)

## ✨ Features

### 📅 Calendar & Reminders
- Interactive monthly calendar view
- Color-coded days — today, selected, has reminder, weekend
- Add reminders with **priority levels** (🔴 High / 🟡 Medium / 🟢 Low)
- Set reminder time (HH:MM)
- Delete reminders with one click

### 😊 Mood Tracker
- Log your daily mood from 7 options
- Happy 😄 · Good 😊 · Neutral 😐 · Sad 😔 · Stressed 😤 · Tired 😴 · Excited 🤩
- Personalized motivational messages
- Mood history visible in Stats page

### 📓 Journal
- Write daily journal entries
- Journal entries automatically linked to today's reminders
- Entries saved and retrievable anytime

### 🎂 Birthday Manager
- Save birthdays for friends & family
- Upcoming birthdays alert (next 30 days)
- Age calculator
- Today's birthday special highlight 🎉

### 📊 Stats & Analytics
- Total reminders count
- This month's reminders
- Mood history log
- Birthday count
- Recent reminders overview

### 📤 Export Data
- Download all reminders as **CSV**
- Download full mood history as **CSV**

### 🎨 Design
- 🌙 Beautiful **dark mode** — deep navy theme
- 💙 Blue accent colors throughout
- 📱 **Mobile responsive** — works on all screen sizes
- ✨ Gradient cards and smooth UI
- 💬 Daily motivational quote

---

## 🛠️ Built With

| Technology | Purpose |
|---|---|
| **Python 3.x** | Core language |
| **Streamlit** | Web framework |
| **JSON** | Local data storage |
| **HTML/CSS** | Custom styling & calendar grid |
| **JavaScript** | UI enhancements |

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/root3016-alt/calendar-reminder-app.git
cd calendar-reminder-app
```

### 2. Install dependencies
```bash
pip install streamlit
```

### 3. Run the app
```bash
streamlit run streamlit_app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

## 📁 Project Structure
```
calendar-reminder-app/
│
├── streamlit_app.py      # Main Streamlit web app
├── main.py               # Desktop tkinter app
├── app.py                # Desktop app UI
├── storage.py            # Data storage functions
├── calendar_view.py      # Calendar widget
├── reminder_manager.py   # Reminder logic
├── notifier.py           # Desktop notifications
├── mood_tracker.py       # Mood tracking
├── birthday.py           # Birthday manager
├── countdown.py          # Countdown timer
├── weather_widget.py     # Weather display
├── quotes.py             # Daily quotes
├── splash.py             # Splash screen
│
├── reminders.json        # Reminders data
├── moods.json            # Mood entries data
├── birthdays.json        # Birthdays data
├── mood_notes.json       # Journal entries data
│
└── README.md             # This file
```

---

## 📊 Data Storage

All data is stored locally as JSON files:

| File | Contents |
|---|---|
| `reminders.json` | All reminders by date |
| `moods.json` | Daily mood entries |
| `birthdays.json` | Saved birthdays |
| `mood_notes.json` | Journal entries |

---

## 🔗 Links

| | |
|---|---|
| 🌐 **Live App** | [https://rcdwx5zu4scbvffx4.streamlit.app](https://rcdwx5zu4scbvffx4.streamlit.app) |
| 💻 **GitHub** | [https://github.com/root3016-alt/calendar-reminder-app](https://github.com/root3016-alt/calendar-reminder-app) |

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**root3016-alt**

Made with ❤️ using Python & Streamlit

---

⭐ **If you like this project, give it a star on GitHub!** ⭐
