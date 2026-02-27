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
    initial_sidebar_state="collapsed"
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

st.markdown("""
<style>
    /* ── Global ── */
    .stApp {
        background-color: #0f0f23 !important;
        color: #eaeaea !important;
    }
    [data-testid="stSidebar"] {
        background-color: #16213e !important;
    }
    [data-testid="stSidebar"] * { color: #eaeaea !important; }

    h1,h2,h3,h4,h5,h6,p,label,span {
        color: #eaeaea !important;
    }

    /* ── Inputs ── */
    .stTextInput input, .stTextArea textarea {
        background-color: #16213e !important;
        color: #eaeaea !important;
        border: 1px solid #4a9eff55 !important;
        border-radius: 8px !important;
    }
    [data-testid="stDateInput"] input {
        background-color: #16213e !important;
        color: #eaeaea !important;
        border: 1px solid #4a9eff55 !important;
    }
    [data-testid="stSelectbox"] > div > div {
        background-color: #16213e !important;
        color: #eaeaea !important;
        border: 1px solid #4a9eff55 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #4a9eff !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    .stDownloadButton > button {
        background-color: #1dd1a1 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        width: 100% !important;
    }

    /* ── Metrics ── */
    [data-testid="metric-container"] {
        background-color: #16213e !important;
        border-radius: 12px !important;
        padding: 12px !important;
        border: 1px solid #4a9eff33 !important;
    }
    [data-testid="stMetricValue"] { color: #4a9eff !important; }
    [data-testid="stMetricLabel"] { color: #aaaaaa !important; }

    /* ── Cards ── */
    .header-box {
        background: linear-gradient(135deg, #16213e, #0f3460);
        border-radius: 15px;
        padding: 20px 25px;
        margin-bottom: 15px;
        border: 1px solid #4a9eff33;
    }
    .quote-box {
        background: #16213e;
        border-left: 4px solid #4a9eff;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-style: italic;
        color: #aaaaaa !important;
    }
    .reminder-card {
        background: #16213e;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 5px 0;
        border-left: 4px solid #4a9eff;
        color: #eaeaea !important;
        font-size: 14px;
    }
    .high  { border-left-color: #ff6b6b !important; }
    .medium{ border-left-color: #ff9f43 !important; }
    .low   { border-left-color: #1dd1a1 !important; }
    .journal { border-left-color: #a29bfe !important; }

    .birthday-card {
        background: #16213e;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 5px 0;
        border-left: 4px solid #fd79a8;
        color: #eaeaea !important;
    }

    /* ── Calendar Grid ── */
    .cal-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 4px;
        text-align: center;
        margin: 8px 0;
    }
    .cal-cell {
        padding: 6px 2px;
        border-radius: 50%;
        font-size: 13px;
        color: #eaeaea;
        min-height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .cal-header {
        font-weight: bold;
        color: #4a9eff !important;
        font-size: 12px;
    }
    .cal-today {
        background: #4a9eff;
        color: white !important;
        border-radius: 50%;
        font-weight: bold;
    }
    .cal-selected {
        background: #1dd1a1;
        color: white !important;
        border-radius: 50%;
        font-weight: bold;
    }
    .cal-reminder {
        color: #ff9f43 !important;
        font-weight: bold;
    }
    .cal-weekend { color: #ff6b6b !important; }
    .cal-empty { color: transparent; }

    /* ── Mood buttons ── */
    .mood-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin: 10px 0;
    }
    .mood-item {
        background: #16213e;
        border-radius: 10px;
        padding: 10px 5px;
        text-align: center;
        border: 1px solid #4a9eff33;
        cursor: pointer;
    }

    /* ── Nav tabs ── */
    .nav-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 6px;
        margin-bottom: 15px;
    }
    .nav-item {
        background: #16213e;
        border-radius: 8px;
        padding: 8px 4px;
        text-align: center;
        font-size: 11px;
        cursor: pointer;
        border: 1px solid #4a9eff33;
        color: #eaeaea !important;
    }
    .nav-active {
        background: #4a9eff !important;
        color: white !important;
        font-weight: bold;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #0f0f23; }
    ::-webkit-scrollbar-thumb { background: #4a9eff; border-radius: 2px; }

    /* ── Mobile responsive ── */
    @media (max-width: 768px) {
        .header-box { padding: 15px; }
        .header-box h1 { font-size: 1.4rem !important; }
        .cal-cell { font-size: 12px; padding: 4px 1px; }
        .mood-grid { grid-template-columns: repeat(4, 1fr); }
        .nav-grid { grid-template-columns: repeat(3, 1fr); }
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1 style="margin:0;color:white!important;font-size:1.6rem">
        📅 Calendar & Reminder App
    </h1>
    <p style="margin:0;color:#aaaaaa!important;font-size:0.9rem">
        Stay organized, never miss a thing!
    </p>
</div>
""", unsafe_allow_html=True)

quote, author = get_quote()
st.markdown(f"""
<div class="quote-box">
    💬 <i>"{quote}"</i> — <b>{author}</b>
</div>
""", unsafe_allow_html=True)

# ── Navigation ───────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "📅 Calendar"

pages = ["📅 Calendar", "😊 Mood", "🎂 Birthdays", "📊 Stats", "📤 Export"]

cols = st.columns(5)
for i, p in enumerate(pages):
    with cols[i]:
        active = "nav-active" if st.session_state.page == p else ""
        if st.button(p, key=f"nav_{p}", use_container_width=True):
            st.session_state.page = p
            st.rerun()

page = st.session_state.page
st.divider()

# ── Today info ───────────────────────────────────────
today_str = datetime.today().strftime("%Y-%m-%d")
moods_data = load_json(MOODS_FILE)
today_mood = moods_data.get(today_str)

info_cols = st.columns(2)
with info_cols[0]:
    st.markdown(f"🕐 **{datetime.now().strftime('%d %b %Y  %H:%M')}**")
with info_cols[1]:
    if today_mood:
        st.markdown(f"**Mood:** {today_mood['emoji']} {today_mood['label']}")

st.divider()

# ── Page: Calendar ───────────────────────────────────
if page == "📅 Calendar":
    st.markdown("### 📅 Select Date")
    selected_date = st.date_input(
        "date", value=date.today(),
        label_visibility="collapsed"
    )
    date_str = selected_date.strftime("%Y-%m-%d")
    reminders_data = load_json(REMINDERS_FILE)

    # ── Proper Calendar Grid using HTML ──
    st.markdown(f"#### 📆 {selected_date.strftime('%B %Y')}")
    cal = calendar.monthcalendar(selected_date.year, selected_date.month)

    cal_html = '<div class="cal-grid">'
    for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        cal_html += f'<div class="cal-cell cal-header">{d}</div>'

    for week in cal:
        for i, day in enumerate(week):
            if day == 0:
                cal_html += '<div class="cal-cell cal-empty">·</div>'
            else:
                day_date = date(selected_date.year, selected_date.month, day)
                day_str_loop = day_date.strftime("%Y-%m-%d")
                has_reminder = day_str_loop in reminders_data
                is_today = day_date == date.today()
                is_selected = day_date == selected_date
                is_weekend = i >= 5

                if is_today:
                    cls = "cal-cell cal-today"
                elif is_selected:
                    cls = "cal-cell cal-selected"
                elif has_reminder:
                    cls = "cal-cell cal-reminder"
                elif is_weekend:
                    cls = "cal-cell cal-weekend"
                else:
                    cls = "cal-cell"

                prefix = "🟡" if has_reminder and not is_today and not is_selected else ""
                cal_html += f'<div class="{cls}">{prefix}{day}</div>'

    cal_html += '</div>'
    st.markdown(cal_html, unsafe_allow_html=True)
    st.markdown("🔵 Today &nbsp; 🟢 Selected &nbsp; 🟡 Has reminder &nbsp; 🔴 Weekend")

    st.divider()

    # ── Reminders ──
    st.markdown(f"### 📝 Reminders — {date_str}")
    reminders = load_json(REMINDERS_FILE)
    day_reminders = reminders.get(date_str, [])

    if day_reminders:
        for i, r in enumerate(day_reminders):
            cls = "reminder-card"
            if "🔴 High" in r: cls += " high"
            elif "🟡 Medium" in r: cls += " medium"
            elif "🟢 Low" in r: cls += " low"
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
    st.markdown("### ➕ Add Reminder")

    priority = st.selectbox("Priority", ["🟡 Medium", "🔴 High", "🟢 Low"])
    time_val = st.text_input("⏰ Time (HH:MM)", placeholder="e.g. 14:30")
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

# ── Page: Mood ───────────────────────────────────────
elif page == "😊 Mood":
    st.markdown("### 😊 How are you feeling today?")

    MOODS = [
        ("😄", "Happy", "#f9ca24"),
        ("😊", "Good", "#6ab04c"),
        ("😐", "Neutral", "#95afc0"),
        ("😔", "Sad", "#778ca3"),
        ("😤", "Stressed", "#e55039"),
        ("😴", "Tired", "#a29bfe"),
        ("🤩", "Excited", "#fd79a8"),
    ]
    MOOD_MESSAGES = {
        "Happy": "Amazing! Happiness is contagious — share it! 💛",
        "Good": "Great! A good day is a gift 🌈",
        "Neutral": "That's okay 🌥️ Be kind to yourself.",
        "Sad": "It's okay 💙 Tough times don't last.",
        "Stressed": "One thing at a time 🧘 You've got this!",
        "Tired": "Rest is productive too 😴",
        "Excited": "Woohoo! 🎉 Channel that energy!",
    }

    existing = moods_data.get(today_str)
    if existing:
        st.success(f"{existing['emoji']} **{existing['label']}** — {MOOD_MESSAGES.get(existing['label'], '')}")

    cols = st.columns(4)
    for i, (emoji, label, color) in enumerate(MOODS):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="mood-item">
                <div style="font-size:1.8rem">{emoji}</div>
                <div style="font-size:0.75rem;color:#aaa">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✓", key=f"mood_{label}", use_container_width=True):
                moods_data[today_str] = {"emoji": emoji, "label": label}
                save_json(MOODS_FILE, moods_data)
                st.success(f"✅ {emoji} {label} saved!")
                st.rerun()

    st.divider()
    st.markdown("### 📓 Journal")
    st.caption("💡 Saved journal appears in today's reminders!")

    mood_notes = load_json(MOOD_NOTES_FILE)
    existing_note = mood_notes.get(today_str, "")
    journal_text = st.text_area(
        "journal", value=existing_note, height=180,
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
            st.success("✅ Journal saved and added to reminders!")
        else:
            st.error("Please write something first!")

# ── Page: Birthdays ──────────────────────────────────
elif page == "🎂 Birthdays":
    st.markdown("### 🎂 Birthday Manager")
    birthdays = load_json(BIRTHDAYS_FILE)
    today = datetime.today()

    st.markdown("#### 🔔 Upcoming (30 days)")
    upcoming = []
    for name, ds in birthdays.items():
        try:
            bday = datetime.strptime(ds, "%Y-%m-%d")
            this_year = bday.replace(year=today.year)
            if this_year < today:
                this_year = this_year.replace(year=today.year + 1)
            diff = (this_year - today).days
            age = today.year - bday.year
            if diff <= 30:
                upcoming.append((name, ds, diff, age + 1))
        except:
            pass

    if upcoming:
        for name, ds, days_left, age in sorted(upcoming, key=lambda x: x[2]):
            if days_left == 0:
                st.success(f"🎉 TODAY — {name} turns {age}!")
            else:
                st.markdown(f"""
                <div class="birthday-card">
                    🎂 <b>{name}</b> — {ds}<br>
                    <small>In {days_left} days · Turns {age}</small>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No upcoming birthdays in next 30 days")

    st.divider()
    st.markdown("#### ➕ Add Birthday")
    new_name = st.text_input("👤 Name")
    new_date = st.date_input("🎂 Birthday", value=date.today())

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
elif page == "📊 Stats":
    st.markdown("### 📊 Stats & Analytics")
    reminders = load_json(REMINDERS_FILE)
    moods = load_json(MOODS_FILE)
    birthdays = load_json(BIRTHDAYS_FILE)

    total = sum(len(v) for v in reminders.values())
    this_month = datetime.today().strftime("%Y-%m")
    month_total = sum(len(v) for k, v in reminders.items()
                      if k.startswith(this_month))

    c1, c2 = st.columns(2)
    c1.metric("📝 Total Reminders", total)
    c2.metric("📅 This Month", month_total)
    c3, c4 = st.columns(2)
    c3.metric("🎂 Birthdays", len(birthdays))
    c4.metric("😊 Mood Entries", len(moods))

    st.divider()
    st.markdown("#### 😊 Recent Moods")
    if moods:
        for ds, mood in sorted(moods.items(), reverse=True)[:7]:
            st.markdown(f"**{ds}** — {mood['emoji']} {mood['label']}")
    else:
        st.info("No mood entries yet")

    st.divider()
    st.markdown("#### 📝 Recent Reminders")
    if reminders:
        for ds, rems in sorted(reminders.items(), reverse=True)[:5]:
            st.markdown(f"**{ds}**")
            for r in rems:
                st.markdown(f"• {r}")
    else:
        st.info("No reminders yet")

# ── Page: Export ─────────────────────────────────────
elif page == "📤 Export":
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