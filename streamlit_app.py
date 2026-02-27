import streamlit as st
import json
import os
from datetime import datetime, date
import calendar
import io
import csv

st.set_page_config(
    page_title="📅 Calendar & Reminder App",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

REMINDERS_FILE = "reminders.json"
MOODS_FILE = "moods.json"
BIRTHDAYS_FILE = "birthdays.json"
MOOD_NOTES_FILE = "mood_notes.json"

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

QUOTES = [
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("The future depends on what you do today.", "Mahatma Gandhi"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Success is not final, failure is not fatal.", "Winston Churchill"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("Spread love everywhere you go.", "Mother Teresa"),
]

def get_quote():
    day = datetime.now().timetuple().tm_yday
    return QUOTES[day % len(QUOTES)]

def build_calendar_html(selected_date, reminders_data):
    cal = calendar.monthcalendar(selected_date.year, selected_date.month)
    html = """
    <style>
    .cal-wrap { width: 100%; overflow-x: auto; }
    .cal-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 4px;
        table-layout: fixed;
    }
    .cal-table th {
        text-align: center;
        padding: 8px 2px;
        color: #4a9eff;
        font-size: 13px;
        font-weight: bold;
        background: #16213e;
        border-radius: 6px;
    }
    .cal-table td {
        text-align: center;
        padding: 6px 2px;
        font-size: 14px;
        color: #eaeaea;
        background: #1a1a2e;
        border-radius: 6px;
        min-width: 32px;
        height: 36px;
        vertical-align: middle;
    }
    .day-today {
        background: #4a9eff !important;
        color: white !important;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    .day-selected {
        background: #1dd1a1 !important;
        color: white !important;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    .day-reminder { color: #ff9f43 !important; font-weight: bold; }
    .day-weekend  { color: #ff6b6b !important; }
    .day-empty    { color: #333 !important; background: transparent !important; }
    @media (max-width: 600px) {
        .cal-table th { font-size: 11px; padding: 5px 1px; }
        .cal-table td { font-size: 12px; padding: 4px 1px; height: 30px; }
        .day-today, .day-selected { width: 24px; height: 24px; }
    }
    </style>
    <div class="cal-wrap">
    <table class="cal-table">
    <tr>
        <th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th>
        <th style="color:#ff6b6b">Sat</th>
        <th style="color:#ff6b6b">Sun</th>
    </tr>
    """
    for week in cal:
        html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                html += '<td class="day-empty">·</td>'
            else:
                day_date     = date(selected_date.year, selected_date.month, day)
                day_str      = day_date.strftime("%Y-%m-%d")
                has_reminder = day_str in reminders_data
                is_today     = day_date == date.today()
                is_selected  = day_date == selected_date
                is_weekend   = i >= 5

                if is_today:
                    html += f'<td><span class="day-today">{day}</span></td>'
                elif is_selected:
                    html += f'<td><span class="day-selected">{day}</span></td>'
                elif has_reminder:
                    html += f'<td><span class="day-reminder">●{day}</span></td>'
                elif is_weekend:
                    html += f'<td><span class="day-weekend">{day}</span></td>'
                else:
                    html += f'<td>{day}</td>'
        html += "</tr>"
    html += "</table></div>"
    return html

st.markdown("""
<style>
    .stApp { background-color: #1a1a2e !important; color: #eaeaea !important; }
    [data-testid="stSidebar"] {
        background-color: #16213e !important;
        border-right: 1px solid #4a9eff33;
    }
    [data-testid="stSidebar"] * { color: #eaeaea !important; }
    h1,h2,h3,h4,h5,h6,p,label,span,div { color: #eaeaea !important; }

    .stTextInput input, .stTextArea textarea {
        background-color: #16213e !important;
        color: #eaeaea !important;
        border: 1px solid #4a9eff55 !important;
        border-radius: 8px !important;
    }
    .stSelectbox select, [data-testid="stSelectbox"] > div {
        background-color: #16213e !important;
        color: #eaeaea !important;
        border: 1px solid #4a9eff55 !important;
    }
    .stDateInput input {
        background-color: #16213e !important;
        color: #eaeaea !important;
        border: 1px solid #4a9eff55 !important;
    }
    .stButton button {
        background-color: #4a9eff !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    .stDownloadButton button {
        background-color: #1dd1a1 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] { color: #4a9eff !important; font-size: 2rem !important; }
    [data-testid="stMetricLabel"] { color: #aaaaaa !important; }
    [data-testid="metric-container"] {
        background-color: #16213e !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 1px solid #4a9eff33 !important;
    }
    .stAlert { background-color: #16213e !important; border-radius: 10px !important; }
    hr { border-color: #4a9eff33 !important; }

    .reminder-card {
        background: #16213e;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        border-left: 4px solid #4a9eff;
        color: #eaeaea !important;
    }
    .high    { border-left-color: #ff6b6b !important; }
    .medium  { border-left-color: #ff9f43 !important; }
    .low     { border-left-color: #1dd1a1 !important; }
    .journal { border-left-color: #a29bfe !important; }

    .quote-box {
        background: #16213e;
        border-left: 4px solid #4a9eff;
        padding: 12px 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #aaaaaa !important;
        font-style: italic;
    }
    .mood-btn {
        background: #16213e;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        border: 1px solid #4a9eff33;
        margin: 4px;
    }
    .birthday-card {
        background: #16213e;
        border-radius: 10px;
        padding: 12px;
        margin: 5px 0;
        border-left: 4px solid #fd79a8;
    }
    .header-box {
        background: linear-gradient(135deg, #16213e, #0f3460);
        border-radius: 15px;
        padding: 20px 30px;
        margin-bottom: 20px;
        border: 1px solid #4a9eff33;
    }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #16213e; }
    ::-webkit-scrollbar-thumb { background: #4a9eff; border-radius: 3px; }

    @media (max-width: 768px) {
        .header-box { padding: 15px !important; }
        .header-box h1 { font-size: 1.3rem !important; }
        .reminder-card { font-size: 13px !important; padding: 8px 10px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1 style="margin:0;color:white!important;">📅 Calendar & Reminder App</h1>
    <p style="margin:0;color:#aaaaaa!important;">Stay organized, never miss a thing!</p>
</div>
""", unsafe_allow_html=True)

quote, author = get_quote()
st.markdown(f"""
<div class="quote-box">
    💬 "{quote}" — <b>{author}</b>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗂️ Navigation")
    page = st.radio(
        "Go to",
        ["📅 Calendar & Reminders",
         "😊 Mood Tracker",
         "🎂 Birthday Manager",
         "📊 Stats & Analytics",
         "📤 Export Data"],
        label_visibility="collapsed"
    )
    st.divider()
    st.markdown(f"🕐 **{datetime.now().strftime('%d %b %Y')}**")
    st.markdown(f"⏰ **{datetime.now().strftime('%H:%M')}**")
    st.divider()
    moods_sb = load_json(MOODS_FILE)
    today_str = datetime.today().strftime("%Y-%m-%d")
    if today_str in moods_sb:
        m = moods_sb[today_str]
        st.markdown(f"**Today's Mood:** {m['emoji']} {m['label']}")
    else:
        st.markdown("**Today's Mood:** Not logged yet")
    st.divider()
    st.markdown("🔵 Today &nbsp; 🟠 Has reminder &nbsp; 🟢 Selected")

# ── Page: Calendar & Reminders ───────────────────────
if page == "📅 Calendar & Reminders":
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("### 📅 Select Date")
        selected_date = st.date_input(
            "date", value=date.today(),
            label_visibility="collapsed"
        )
        date_str = selected_date.strftime("%Y-%m-%d")
        reminders_data = load_json(REMINDERS_FILE)

        st.markdown(f"#### 📆 {selected_date.strftime('%B %Y')}")
        st.markdown(build_calendar_html(selected_date, reminders_data),
                    unsafe_allow_html=True)
        st.markdown("🔵 Today &nbsp; 🟢 Selected &nbsp; 🟠 Has reminder")

    with col2:
        st.markdown(f"### 📝 Reminders for {date_str}")
        reminders = load_json(REMINDERS_FILE)
        day_reminders = reminders.get(date_str, [])

        if day_reminders:
            for i, r in enumerate(day_reminders):
                cls = "reminder-card"
                if "🔴 High"    in r: cls += " high"
                elif "🟡 Medium" in r: cls += " medium"
                elif "🟢 Low"    in r: cls += " low"
                elif "📓 Journal" in r: cls += " journal"
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.markdown(f'<div class="{cls}">{r}</div>',
                                unsafe_allow_html=True)
                with c2:
                    if st.button("🗑", key=f"del_{i}_{date_str}"):
                        reminders[date_str].remove(r)
                        if not reminders[date_str]:
                            del reminders[date_str]
                        save_json(REMINDERS_FILE, reminders)
                        st.rerun()
        else:
            st.info("📭 No reminders for this day")

        st.divider()
        st.markdown("#### ➕ Add Reminder")
        priority = st.selectbox("Priority", ["🟡 Medium", "🔴 High", "🟢 Low"])
        c1, c2 = st.columns(2)
        with c1:
            time_val = st.text_input("⏰ Time (HH:MM)", placeholder="e.g. 14:30")
        with c2:
            note = st.text_input("📌 Note", placeholder="e.g. Team Meeting")

        if st.button("➕ Add Reminder", type="primary", use_container_width=True):
            if note.strip():
                reminder_text = (f"{time_val} | {priority} | {note}"
                                 if time_val.strip()
                                 else f"{priority} | {note}")
                if date_str not in reminders:
                    reminders[date_str] = []
                reminders[date_str].append(reminder_text)
                save_json(REMINDERS_FILE, reminders)
                st.success("✅ Reminder added!")
                st.rerun()
            else:
                st.error("Please enter a note!")

# ── Page: Mood Tracker ───────────────────────────────
elif page == "😊 Mood Tracker":
    st.markdown("### 😊 How are you feeling today?")

    MOODS = [
        ("😄", "Happy",    "#f9ca24"),
        ("😊", "Good",     "#6ab04c"),
        ("😐", "Neutral",  "#95afc0"),
        ("😔", "Sad",      "#778ca3"),
        ("😤", "Stressed", "#e55039"),
        ("😴", "Tired",    "#a29bfe"),
        ("🤩", "Excited",  "#fd79a8"),
    ]
    MOOD_MESSAGES = {
        "Happy":   "Amazing! Happiness is contagious — share it! 💛",
        "Good":    "Great! A good day is a gift 🌈 Make the most of it!",
        "Neutral": "That's okay 🌥️ Not every day needs to be extraordinary.",
        "Sad":     "It's okay 💙 Tough times don't last, tough people do.",
        "Stressed":"One thing at a time 🧘 You've got this!",
        "Tired":   "Rest is productive too 😴 Be kind to yourself.",
        "Excited": "Woohoo! 🎉 Channel that energy into something great!",
    }

    today_str  = datetime.today().strftime("%Y-%m-%d")
    moods_data = load_json(MOODS_FILE)
    existing   = moods_data.get(today_str)

    if existing:
        st.success(f"Today's mood: {existing['emoji']} **{existing['label']}** — {MOOD_MESSAGES.get(existing['label'], '')}")

    st.markdown("#### Select your mood:")
    cols = st.columns(4)
    for i, (emoji, label, color) in enumerate(MOODS):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="mood-btn">
                <div style="font-size:2rem">{emoji}</div>
                <div style="font-size:0.8rem">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select", key=f"mood_{label}", use_container_width=True):
                moods_data[today_str] = {"emoji": emoji, "label": label}
                save_json(MOODS_FILE, moods_data)
                st.success(f"✅ {emoji} {label} — {MOOD_MESSAGES.get(label, '')}")
                st.rerun()

    st.divider()
    st.markdown("### 📓 Journal")
    st.caption("💡 Your journal will appear in today's reminder list!")

    mood_notes    = load_json(MOOD_NOTES_FILE)
    existing_note = mood_notes.get(today_str, "")
    journal_text  = st.text_area(
        "Write your thoughts...",
        value=existing_note,
        height=200,
        label_visibility="collapsed",
        placeholder="Write about your day here..."
    )

    if st.button("💾 Save Journal", type="primary", use_container_width=True):
        if journal_text.strip():
            mood_notes[today_str] = journal_text
            save_json(MOOD_NOTES_FILE, mood_notes)
            reminders = load_json(REMINDERS_FILE)
            if today_str not in reminders:
                reminders[today_str] = []
            reminders[today_str] = [
                r for r in reminders[today_str]
                if not r.startswith("📓 Journal:")
            ]
            short = (journal_text[:60] + "..."
                     if len(journal_text) > 60 else journal_text)
            reminders[today_str].append(f"📓 Journal: {short}")
            save_json(REMINDERS_FILE, reminders)
            st.success("✅ Journal saved and added to today's reminders!")
        else:
            st.error("Please write something first!")

# ── Page: Birthday Manager ───────────────────────────
elif page == "🎂 Birthday Manager":
    st.markdown("### 🎂 Birthday Manager")
    birthdays = load_json(BIRTHDAYS_FILE)
    today     = datetime.today()

    st.markdown("#### 🔔 Upcoming (next 30 days)")
    upcoming = []
    for name, ds in birthdays.items():
        try:
            bday      = datetime.strptime(ds, "%Y-%m-%d")
            this_year = bday.replace(year=today.year)
            if this_year < today:
                this_year = this_year.replace(year=today.year + 1)
            diff = (this_year - today).days
            age  = today.year - bday.year
            if diff <= 30:
                upcoming.append((name, ds, diff, age + 1))
        except:
            pass

    if upcoming:
        for name, ds, days_left, age in sorted(upcoming, key=lambda x: x[2]):
            if days_left == 0:
                st.success(f"🎉 **TODAY** — {name} turns {age}!")
            else:
                st.markdown(f"""
                <div class="birthday-card">
                    🎂 <b>{name}</b> — {ds} | In {days_left} days | Turns {age}
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No upcoming birthdays in next 30 days")

    st.divider()
    st.markdown("#### ➕ Add Birthday")
    c1, c2 = st.columns(2)
    with c1:
        new_name = st.text_input("👤 Name")
    with c2:
        new_date = st.date_input("🎂 Date", value=date.today())

    if st.button("🎂 Save Birthday", type="primary", use_container_width=True):
        if new_name.strip():
            birthdays[new_name] = new_date.strftime("%Y-%m-%d")
            save_json(BIRTHDAYS_FILE, birthdays)
            st.success(f"✅ {new_name}'s birthday saved!")
            st.rerun()
        else:
            st.error("Please enter a name!")

    st.divider()
    st.markdown("#### 📋 All Birthdays")
    if birthdays:
        for name, ds in birthdays.items():
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
                <div class="birthday-card">
                    🎂 <b>{name}</b> — {ds}
                </div>""", unsafe_allow_html=True)
            with c2:
                if st.button("🗑", key=f"del_b_{name}"):
                    del birthdays[name]
                    save_json(BIRTHDAYS_FILE, birthdays)
                    st.rerun()
    else:
        st.info("No birthdays saved yet")

# ── Page: Stats ──────────────────────────────────────
elif page == "📊 Stats & Analytics":
    st.markdown("### 📊 Stats & Analytics")
    reminders  = load_json(REMINDERS_FILE)
    moods      = load_json(MOODS_FILE)
    birthdays  = load_json(BIRTHDAYS_FILE)

    total       = sum(len(v) for v in reminders.values())
    this_month  = datetime.today().strftime("%Y-%m")
    month_total = sum(len(v) for k, v in reminders.items()
                      if k.startswith(this_month))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📝 Total Reminders", total)
    c2.metric("📅 This Month", month_total)
    c3.metric("🎂 Birthdays", len(birthdays))
    c4.metric("😊 Mood Entries", len(moods))

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 😊 Mood History")
        if moods:
            for ds, mood in sorted(moods.items(), reverse=True)[:10]:
                st.markdown(f"**{ds}** — {mood['emoji']} {mood['label']}")
        else:
            st.info("No mood entries yet")
    with col2:
        st.markdown("#### 📝 Recent Reminders")
        if reminders:
            for ds, rems in sorted(reminders.items(), reverse=True)[:5]:
                st.markdown(f"**{ds}**")
                for r in rems:
                    st.markdown(f"• {r}")
        else:
            st.info("No reminders yet")

# ── Page: Export ─────────────────────────────────────
elif page == "📤 Export Data":
    st.markdown("### 📤 Export Your Data")
    reminders = load_json(REMINDERS_FILE)

    if reminders:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Date", "Reminder"])
        for ds, rems in sorted(reminders.items()):
            for r in rems:
                writer.writerow([ds, r])
        st.download_button(
            "📥 Download Reminders CSV",
            data=output.getvalue(),
            file_name="reminders_export.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )
    else:
        st.info("No reminders to export yet")

    st.divider()
    moods = load_json(MOODS_FILE)
    if moods:
        mood_out = io.StringIO()
        mw = csv.writer(mood_out)
        mw.writerow(["Date", "Emoji", "Mood"])
        for ds, mood in sorted(moods.items()):
            mw.writerow([ds, mood["emoji"], mood["label"]])
        st.download_button(
            "📥 Download Mood History CSV",
            data=mood_out.getvalue(),
            file_name="mood_export.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No mood entries to export yet")