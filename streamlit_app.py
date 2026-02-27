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

def build_calendar_html(selected_date, reminders_data):
    cal = calendar.monthcalendar(selected_date.year, selected_date.month)
    html = """
    <style>
    .cal-wrap { width:100%; overflow-x:auto; margin:10px 0; }
    .cal-table {
        width:100%; border-collapse:separate;
        border-spacing:3px; table-layout:fixed;
    }
    .cal-table th {
        text-align:center; padding:10px 2px;
        color:#4a9eff; font-size:12px; font-weight:700;
        letter-spacing:1px; text-transform:uppercase;
        background:#1a2744; border-radius:6px;
        font-family:'Segoe UI',sans-serif;
    }
    .cal-table td {
        text-align:center; padding:8px 2px;
        font-size:14px; color:#c8d8e8;
        background:#16213e; border-radius:8px;
        height:38px; vertical-align:middle;
        font-family:'Segoe UI',sans-serif;
    }
    .day-today {
        background:#4a9eff!important; color:white!important;
        border-radius:50%; width:30px; height:30px;
        display:inline-flex; align-items:center;
        justify-content:center; font-weight:bold;
        box-shadow:0 0 10px #4a9eff88;
    }
    .day-selected {
        background:#1dd1a1!important; color:white!important;
        border-radius:50%; width:30px; height:30px;
        display:inline-flex; align-items:center;
        justify-content:center; font-weight:bold;
        box-shadow:0 0 10px #1dd1a188;
    }
    .day-reminder { color:#ff9f43!important; font-weight:bold; }
    .day-weekend  { color:#ff6b6b!important; }
    .day-empty    { color:transparent!important; background:transparent!important; }
    @media(max-width:600px){
        .cal-table th { font-size:10px; padding:6px 1px; }
        .cal-table td { font-size:12px; padding:5px 1px; height:30px; }
        .day-today,.day-selected { width:24px; height:24px; font-size:11px; }
    }
    </style>
    <div class="cal-wrap">
    <table class="cal-table"><tr>
        <th>MON</th><th>TUE</th><th>WED</th><th>THU</th><th>FRI</th>
        <th style="color:#ff6b6b">SAT</th>
        <th style="color:#ff6b6b">SUN</th>
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

# ── CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family:'Inter','Segoe UI',sans-serif !important; }

.stApp {
    background:linear-gradient(135deg,#0d1117 0%,#0f1923 50%,#0d1117 100%) !important;
    color:#eaeaea !important;
}
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0f1923 0%,#16213e 100%) !important;
    border-right:1px solid #4a9eff22 !important;
}
[data-testid="stSidebar"] * { color:#c8d8e8 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color:white !important; }

h1,h2,h3,h4,h5,h6 { color:white !important; font-weight:700 !important; }
p,label,span,div   { color:#c8d8e8 !important; }

.stTextInput input,.stTextArea textarea {
    background:#16213e !important; color:#eaeaea !important;
    border:1px solid #4a9eff44 !important; border-radius:10px !important;
    font-size:14px !important;
}
.stTextInput input:focus,.stTextArea textarea:focus {
    border-color:#4a9eff !important;
    box-shadow:0 0 0 2px #4a9eff22 !important;
}
[data-testid="stDateInput"] input {
    background:#16213e !important; color:#eaeaea !important;
    border:1px solid #4a9eff44 !important; border-radius:10px !important;
}
[data-testid="stSelectbox"] > div > div {
    background:#16213e !important; color:#eaeaea !important;
    border:1px solid #4a9eff44 !important; border-radius:10px !important;
}
.stButton > button {
    background:linear-gradient(135deg,#4a9eff,#2980b9) !important;
    color:white !important; border:none !important;
    border-radius:10px !important; font-weight:600 !important;
    font-size:14px !important; padding:10px 20px !important;
    box-shadow:0 4px 15px #4a9eff33 !important;
    transition:all 0.2s !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 6px 20px #4a9eff55 !important;
}
.stDownloadButton > button {
    background:linear-gradient(135deg,#1dd1a1,#00b894) !important;
    color:white !important; border:none !important;
    border-radius:10px !important; font-weight:600 !important;
}
[data-testid="metric-container"] {
    background:linear-gradient(135deg,#16213e,#1a2744) !important;
    border-radius:15px !important; padding:20px !important;
    border:1px solid #4a9eff33 !important;
    box-shadow:0 4px 20px #00000044 !important;
}
[data-testid="stMetricValue"] { color:#4a9eff !important; font-size:2rem !important; font-weight:700 !important; }
[data-testid="stMetricLabel"] { color:#8899aa !important; font-size:12px !important; }
.stAlert { background:#16213e !important; border-radius:12px !important; border:1px solid #4a9eff22 !important; }
hr { border-color:#4a9eff22 !important; margin:20px 0 !important; }

/* Cards */
.header-box {
    background:linear-gradient(135deg,#16213e 0%,#0f3460 100%);
    border-radius:20px; padding:25px 35px; margin-bottom:15px;
    border:1px solid #4a9eff33; box-shadow:0 8px 32px #00000055;
}
.quote-box {
    background:linear-gradient(135deg,#16213e,#1a2744);
    border-left:3px solid #4a9eff; padding:12px 20px;
    border-radius:12px; margin-bottom:15px;
    color:#8899aa !important; font-style:italic; font-size:13px;
}
.reminder-card {
    background:linear-gradient(135deg,#16213e,#1a2744);
    border-radius:12px; padding:14px 18px; margin:8px 0;
    border-left:4px solid #4a9eff; color:#eaeaea !important;
    font-size:14px; box-shadow:0 2px 10px #00000033;
}
.high    { border-left-color:#ff6b6b !important; }
.medium  { border-left-color:#ff9f43 !important; }
.low     { border-left-color:#1dd1a1 !important; }
.journal { border-left-color:#a29bfe !important; }
.mood-btn {
    background:linear-gradient(135deg,#16213e,#1a2744);
    border-radius:12px; padding:12px 8px; text-align:center;
    border:1px solid #4a9eff33; margin:4px 0;
}
.birthday-card {
    background:linear-gradient(135deg,#16213e,#1a2744);
    border-radius:12px; padding:14px 18px; margin:8px 0;
    border-left:4px solid #fd79a8; color:#eaeaea !important;
}
.stats-box {
    background:linear-gradient(135deg,#16213e,#1a2744);
    border-radius:12px; padding:10px 15px; margin:4px 0;
    border:1px solid #4a9eff22;
}
.section-title {
    font-size:1.1rem; font-weight:700; color:white !important;
    margin:15px 0 10px 0; padding-bottom:8px;
    border-bottom:1px solid #4a9eff22;
}
.footer-bar {
    background:linear-gradient(135deg,#16213e,#0f3460);
    border-radius:12px; padding:10px 20px; margin-top:20px;
    border:1px solid #4a9eff22; font-size:12px; color:#8899aa !important;
    display:flex; justify-content:space-between; align-items:center;
}
.sidebar-info {
    background:#1a2744; border-radius:12px;
    padding:12px 15px; margin:5px 0; border:1px solid #4a9eff22;
}

/* Mobile nav tabs */
.mobile-nav {
    display:none;
    grid-template-columns:repeat(5,1fr);
    gap:4px; margin-bottom:15px;
}
.mobile-nav-btn {
    background:#16213e; border-radius:8px; padding:8px 4px;
    text-align:center; font-size:10px; border:1px solid #4a9eff22;
    color:#c8d8e8 !important; cursor:pointer;
}
.mobile-nav-active {
    background:linear-gradient(135deg,#4a9eff,#2980b9) !important;
    color:white !important; font-weight:bold;
}

::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:#0d1117; }
::-webkit-scrollbar-thumb { background:#4a9eff66; border-radius:3px; }

/* ── Mobile Responsive ── */
@media(max-width:768px){
    .header-box { padding:15px 20px !important; }
    .header-box h1 { font-size:1.2rem !important; }
    .reminder-card { font-size:12px !important; padding:10px 12px !important; }
    .mood-btn { padding:8px 4px !important; }
    [data-testid="stMetricValue"] { font-size:1.5rem !important; }
    /* Hide sidebar toggle arrow on mobile */
    [data-testid="collapsedControl"] { display:none !important; }
    /* Show mobile nav */
    .mobile-nav { display:grid !important; }
}
</style>
""", unsafe_allow_html=True)

now       = datetime.now()
today_str = datetime.today().strftime("%Y-%m-%d")
moods_all = load_json(MOODS_FILE)
mood_today = moods_all.get(today_str)

# ── Header ───────────────────────────────────────────
st.markdown(f"""
<div class="header-box">
    <h1 style="margin:0;color:white!important;font-size:1.8rem;font-weight:800">
        📅 Calendar & Reminder App
    </h1>
    <p style="margin:4px 0 0;color:#8899aa!important;font-size:0.85rem">
        🕐 {now.strftime('%A, %d %B %Y  |  %H:%M')}
        &nbsp;|&nbsp;
        {f"Mood: {mood_today['emoji']} {mood_today['label']}" if mood_today else "Mood: Not logged"}
    </p>
</div>
""", unsafe_allow_html=True)

quote, author = get_quote()
st.markdown(f"""
<div class="quote-box">
    💬 <i>"{quote}"</i> — <b style="color:#4a9eff">{author}</b>
</div>
""", unsafe_allow_html=True)

# ── Sidebar (laptop) ─────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px">
        <div style="font-size:2.5rem">📅</div>
        <div style="font-weight:700;font-size:1rem;color:white!important">Calendar App</div>
        <div style="font-size:11px;color:#8899aa!important">Stay Organized</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["📅 Calendar & Reminders",
         "😊 Mood Tracker",
         "🎂 Birthday Manager",
         "📊 Stats & Analytics",
         "📤 Export Data"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown(f"""
    <div class="sidebar-info">
        <div style="font-size:11px;color:#8899aa!important">TODAY'S MOOD</div>
        <div style="font-size:1.1rem;color:white!important">
            {f"{mood_today['emoji']} {mood_today['label']}" if mood_today else "Not logged yet"}
        </div>
    </div>
    <div class="sidebar-info">
        <div style="font-size:11px;color:#8899aa!important">DATE</div>
        <div style="font-size:0.95rem;color:white!important">{now.strftime('%d %b %Y')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="font-size:11px;color:#8899aa!important;line-height:2">
        🔵 Today &nbsp;|&nbsp; 🟢 Selected<br>
        🟠 Has reminder &nbsp;|&nbsp; 🔴 Weekend
    </div>
    """, unsafe_allow_html=True)

# ── Mobile Navigation (tabs) ─────────────────────────
if "page" not in st.session_state:
    st.session_state.page = page

# Mobile nav buttons
mob_cols = st.columns(5)
pages_list = [
    ("📅", "Calendar"),
    ("😊", "Mood"),
    ("🎂", "Birthdays"),
    ("📊", "Stats"),
    ("📤", "Export"),
]
page_map = {
    "Calendar":  "📅 Calendar & Reminders",
    "Mood":      "😊 Mood Tracker",
    "Birthdays": "🎂 Birthday Manager",
    "Stats":     "📊 Stats & Analytics",
    "Export":    "📤 Export Data",
}
for i, (icon, label) in enumerate(pages_list):
    with mob_cols[i]:
        if st.button(f"{icon}\n{label}", key=f"mob_{label}",
                     use_container_width=True):
            st.session_state.page = page_map[label]
            st.rerun()

# Use sidebar page on laptop, session state on mobile
active_page = st.session_state.get("page", page)
# Sync sidebar selection
if page != active_page:
    active_page = page

st.divider()

# ── Page: Calendar & Reminders ───────────────────────
if active_page == "📅 Calendar & Reminders":
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown('<div class="section-title">📅 Select Date</div>',
                    unsafe_allow_html=True)
        selected_date  = st.date_input("d", value=date.today(),
                                       label_visibility="collapsed")
        date_str       = selected_date.strftime("%Y-%m-%d")
        reminders_data = load_json(REMINDERS_FILE)

        st.markdown(f'<div class="section-title">📆 {selected_date.strftime("%B %Y")}</div>',
                    unsafe_allow_html=True)
        st.markdown(build_calendar_html(selected_date, reminders_data),
                    unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:11px;color:#8899aa!important;margin-top:5px">
            🔵 Today &nbsp; 🟢 Selected &nbsp; 🟠 Reminder &nbsp; 🔴 Weekend
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="section-title">📝 Reminders — {date_str}</div>',
                    unsafe_allow_html=True)
        reminders     = load_json(REMINDERS_FILE)
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
        st.markdown('<div class="section-title">➕ Add Reminder</div>',
                    unsafe_allow_html=True)
        priority = st.selectbox("Priority", ["🟡 Medium", "🔴 High", "🟢 Low"])
        c1, c2   = st.columns(2)
        with c1:
            time_val = st.text_input("⏰ Time (HH:MM)", placeholder="14:30")
        with c2:
            note = st.text_input("📌 Note", placeholder="Team Meeting")

        if st.button("➕ Add Reminder", type="primary", use_container_width=True):
            if note.strip():
                rt = (f"{time_val} | {priority} | {note}"
                      if time_val.strip() else f"{priority} | {note}")
                if date_str not in reminders:
                    reminders[date_str] = []
                reminders[date_str].append(rt)
                save_json(REMINDERS_FILE, reminders)
                st.success("✅ Reminder added!")
                st.rerun()
            else:
                st.error("Please enter a note!")

# ── Page: Mood Tracker ───────────────────────────────
elif active_page == "😊 Mood Tracker":
    st.markdown('<div class="section-title">😊 How are you feeling today?</div>',
                unsafe_allow_html=True)
    MOODS = [
        ("😄","Happy","#f9ca24"),("😊","Good","#6ab04c"),
        ("😐","Neutral","#95afc0"),("😔","Sad","#778ca3"),
        ("😤","Stressed","#e55039"),("😴","Tired","#a29bfe"),
        ("🤩","Excited","#fd79a8"),
    ]
    MOOD_MESSAGES = {
        "Happy":"Amazing! Happiness is contagious — share it! 💛",
        "Good":"Great! A good day is a gift 🌈",
        "Neutral":"That's okay 🌥️ Be kind to yourself.",
        "Sad":"It's okay 💙 Tough times don't last.",
        "Stressed":"One thing at a time 🧘 You've got this!",
        "Tired":"Rest is productive too 😴",
        "Excited":"Woohoo! 🎉 Channel that energy!",
    }
    moods_data = load_json(MOODS_FILE)
    existing   = moods_data.get(today_str)
    if existing:
        st.success(f"{existing['emoji']} **{existing['label']}** — {MOOD_MESSAGES.get(existing['label'],'')}")

    cols = st.columns(4)
    for i, (emoji, label, color) in enumerate(MOODS):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="mood-btn">
                <div style="font-size:1.8rem">{emoji}</div>
                <div style="font-size:0.7rem;color:#8899aa!important">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✓", key=f"mood_{label}", use_container_width=True):
                moods_data[today_str] = {"emoji":emoji,"label":label}
                save_json(MOODS_FILE, moods_data)
                st.success(f"✅ {emoji} {label} saved!")
                st.rerun()

    st.divider()
    st.markdown('<div class="section-title">📓 Journal</div>', unsafe_allow_html=True)
    st.caption("💡 Your journal will appear in today's reminder list!")
    mood_notes    = load_json(MOOD_NOTES_FILE)
    existing_note = mood_notes.get(today_str, "")
    journal_text  = st.text_area("j", value=existing_note, height=200,
                                  label_visibility="collapsed",
                                  placeholder="Write about your day here...")
    if st.button("💾 Save Journal", type="primary", use_container_width=True):
        if journal_text.strip():
            mood_notes[today_str] = journal_text
            save_json(MOOD_NOTES_FILE, mood_notes)
            reminders = load_json(REMINDERS_FILE)
            if today_str not in reminders:
                reminders[today_str] = []
            reminders[today_str] = [r for r in reminders[today_str]
                                     if not r.startswith("📓 Journal:")]
            short = journal_text[:60]+"..." if len(journal_text)>60 else journal_text
            reminders[today_str].append(f"📓 Journal: {short}")
            save_json(REMINDERS_FILE, reminders)
            st.success("✅ Journal saved and added to today's reminders!")
        else:
            st.error("Please write something first!")

# ── Page: Birthday Manager ───────────────────────────
elif active_page == "🎂 Birthday Manager":
    st.markdown('<div class="section-title">🎂 Birthday Manager</div>', unsafe_allow_html=True)
    birthdays = load_json(BIRTHDAYS_FILE)
    today_dt  = datetime.today()

    st.markdown('<div class="section-title">🔔 Upcoming (30 days)</div>', unsafe_allow_html=True)
    upcoming = []
    for name, ds in birthdays.items():
        try:
            bday      = datetime.strptime(ds,"%Y-%m-%d")
            this_year = bday.replace(year=today_dt.year)
            if this_year < today_dt:
                this_year = this_year.replace(year=today_dt.year+1)
            diff = (this_year-today_dt).days
            age  = today_dt.year-bday.year
            if diff <= 30:
                upcoming.append((name,ds,diff,age+1))
        except: pass

    if upcoming:
        for name,ds,days_left,age in sorted(upcoming,key=lambda x:x[2]):
            if days_left == 0:
                st.success(f"🎉 TODAY — {name} turns {age}!")
            else:
                st.markdown(f"""
                <div class="birthday-card">
                    🎂 <b style="color:white!important">{name}</b>
                    <span style="color:#8899aa!important;font-size:12px"> — {ds}</span><br>
                    <small style="color:#fd79a8!important">In {days_left} days · Turns {age}</small>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No upcoming birthdays in next 30 days")

    st.divider()
    st.markdown('<div class="section-title">➕ Add Birthday</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: new_name = st.text_input("👤 Name")
    with c2: new_date = st.date_input("🎂 Date", value=date.today())
    if st.button("🎂 Save Birthday", type="primary", use_container_width=True):
        if new_name.strip():
            birthdays[new_name] = new_date.strftime("%Y-%m-%d")
            save_json(BIRTHDAYS_FILE, birthdays)
            st.success(f"✅ {new_name}'s birthday saved!")
            st.rerun()
        else:
            st.error("Please enter a name!")

    st.divider()
    st.markdown('<div class="section-title">📋 All Birthdays</div>', unsafe_allow_html=True)
    if birthdays:
        for name,ds in birthdays.items():
            c1,c2 = st.columns([5,1])
            with c1:
                st.markdown(f"""
                <div class="birthday-card">
                    🎂 <b style="color:white!important">{name}</b>
                    <span style="color:#8899aa!important"> — {ds}</span>
                </div>""", unsafe_allow_html=True)
            with c2:
                if st.button("🗑", key=f"del_b_{name}"):
                    del birthdays[name]
                    save_json(BIRTHDAYS_FILE, birthdays)
                    st.rerun()
    else:
        st.info("No birthdays saved yet")

# ── Page: Stats ──────────────────────────────────────
elif active_page == "📊 Stats & Analytics":
    st.markdown('<div class="section-title">📊 Stats & Analytics</div>', unsafe_allow_html=True)
    reminders = load_json(REMINDERS_FILE)
    moods     = load_json(MOODS_FILE)
    birthdays = load_json(BIRTHDAYS_FILE)
    total       = sum(len(v) for v in reminders.values())
    this_month  = datetime.today().strftime("%Y-%m")
    month_total = sum(len(v) for k,v in reminders.items() if k.startswith(this_month))
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📝 Total", total)
    c2.metric("📅 This Month", month_total)
    c3.metric("🎂 Birthdays", len(birthdays))
    c4.metric("😊 Moods", len(moods))
    st.divider()
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">😊 Mood History</div>', unsafe_allow_html=True)
        if moods:
            for ds,mood in sorted(moods.items(),reverse=True)[:10]:
                st.markdown(f"""
                <div class="stats-box">
                    <span style="color:#8899aa!important;font-size:12px">{ds}</span>
                    &nbsp; {mood['emoji']}
                    <b style="color:white!important">{mood['label']}</b>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No mood entries yet")
    with col2:
        st.markdown('<div class="section-title">📝 Recent Reminders</div>', unsafe_allow_html=True)
        if reminders:
            for ds,rems in sorted(reminders.items(),reverse=True)[:5]:
                st.markdown(f"""
                <div class="stats-box">
                    <div style="color:#4a9eff!important;font-size:12px;font-weight:600">{ds}</div>
                    {"".join(f'<div style="color:#c8d8e8!important;font-size:13px">• {r}</div>' for r in rems)}
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No reminders yet")

# ── Page: Export ─────────────────────────────────────
elif active_page == "📤 Export Data":
    st.markdown('<div class="section-title">📤 Export Your Data</div>', unsafe_allow_html=True)
    reminders = load_json(REMINDERS_FILE)
    if reminders:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Date","Reminder"])
        for ds,rems in sorted(reminders.items()):
            for r in rems: writer.writerow([ds,r])
        st.download_button("📥 Download Reminders CSV",
                           data=output.getvalue(),
                           file_name="reminders_export.csv",
                           mime="text/csv", type="primary",
                           use_container_width=True)
    else:
        st.info("No reminders to export yet")
    st.divider()
    moods = load_json(MOODS_FILE)
    if moods:
        mood_out = io.StringIO()
        mw = csv.writer(mood_out)
        mw.writerow(["Date","Emoji","Mood"])
        for ds,mood in sorted(moods.items()):
            mw.writerow([ds,mood["emoji"],mood["label"]])
        st.download_button("📥 Download Mood History CSV",
                           data=mood_out.getvalue(),
                           file_name="mood_export.csv",
                           mime="text/csv", use_container_width=True)
    else:
        st.info("No mood entries to export yet")

# ── Footer ────────────────────────────────────────────
st.markdown(f"""
<div class="footer-bar">
    <span style="color:#8899aa!important">🔔 Notifications active &nbsp;|&nbsp; 📁 Auto-saved</span>
    <span style="color:#4a9eff!important">🕐 {datetime.now().strftime('%H:%M:%S')}</span>
</div>
""", unsafe_allow_html=True)