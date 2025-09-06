import streamlit as st
import json
import os
from datetime import datetime, timedelta
import hashlib

DATA_FILE = "counters.json"
USERS_FILE = "users.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed_password):
    return hash_password(password) == hashed_password


st.set_page_config(
    page_title="Multi Counter & Time Calculator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --bg-card: #ffffff;
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
    --text-muted: #718096;
    --border-color: #e2e8f0;
    --shadow-color: rgba(0, 0, 0, 0.1);
    --accent-color: #667eea;
    --accent-secondary: #764ba2;
    --accent-bg: #f7fafc;
    --button-bg: #ffffff;
    --button-border: #e2e8f0;
    --button-hover: #f7fafc;
    --success-color: #48bb78;
    --danger-color: #f56565;
    --warning-color: #ed8936;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-card: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: #475569;
        --shadow-color: rgba(0, 0, 0, 0.3);
        --accent-color: #818cf8;
        --accent-secondary: #a855f7;
        --accent-bg: #1e293b;
        --button-bg: #475569;
        --button-border: #64748b;
        --button-hover: #64748b;
        --success-color: #34d399;
        --danger-color: #f87171;
        --warning-color: #fbbf24;
    }
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.stApp {
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}

.main .block-container {
    padding: 1rem;
    max-width: 1200px;
}

.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 70vh;
    padding: 2rem;
}

.login-card {
    background: var(--bg-card);
    border-radius: 20px;
    padding: 3rem;
    box-shadow: 0 20px 40px var(--shadow-color);
    border: 1px solid var(--border-color);
    max-width: 450px;
    width: 100%;
    backdrop-filter: blur(10px);
}

.login-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.login-subtitle {
    text-align: center;
    color: var(--text-muted);
    margin-bottom: 2rem;
    font-size: 1.1rem;
}

.hero-container {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
    border-radius: 20px;
    margin: 2rem 0;
    color: white;
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    opacity: 0.3;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
}

.hero-subtitle {
    font-size: 1.3rem;
    margin-bottom: 3rem;
    opacity: 0.9;
    position: relative;
    z-index: 1;
}

.hero-features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
    position: relative;
    z-index: 1;
}

.feature-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.feature-card:hover {
    transform: translateY(-8px);
    background: rgba(255, 255, 255, 0.25);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
}

.feature-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.feature-description {
    opacity: 0.9;
    line-height: 1.6;
}

.user-bar {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 12px var(--shadow-color);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-primary);
    font-weight: 500;
}

.logout-btn {
    background: var(--danger-color) !important;
    color: white !important;
    border: none !important;
    padding: 0.5rem 1rem !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

.logout-btn:hover {
    background: #e53e3e !important;
    transform: translateY(-1px) !important;
}

.counter-card {
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    background: var(--bg-card);
    box-shadow: 0 4px 12px var(--shadow-color);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.counter-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-color), var(--accent-secondary));
}

.counter-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px var(--shadow-color);
}

.counter-name {
    text-align: center;
    font-weight: 600;
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: 12px;
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.counter-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--accent-color);
    padding: 1rem;
    background: var(--accent-bg);
    border: 2px solid var(--accent-color);
    border-radius: 12px;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 8px var(--shadow-color);
}

.stButton > button {
    width: 100%;
    height: 50px;
    font-weight: 600;
    border-radius: 10px;
    font-size: 15px;
    background-color: var(--button-bg) !important;
    border: 1px solid var(--button-border) !important;
    color: var(--text-primary) !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px var(--shadow-color) !important;
}

.stButton > button:hover {
    background-color: var(--button-hover) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 16px var(--shadow-color) !important;
}

button[key*="inc_"] {
    background: linear-gradient(135deg, var(--success-color), #38a169) !important;
    color: white !important;
    border: none !important;
}

button[key*="dec_"] {
    background: linear-gradient(135deg, var(--danger-color), #e53e3e) !important;
    color: white !important;
    border: none !important;
}

button[key*="reset_"] {
    background: linear-gradient(135deg, #718096, #4a5568) !important;
    color: white !important;
    border: none !important;
}

.time-calculator-container {
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 20px;
    margin: 2rem 0;
    border: 1px solid var(--border-color);
    box-shadow: 0 8px 24px var(--shadow-color);
    position: relative;
}

.time-calculator-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-color), var(--accent-secondary));
    border-radius: 20px 20px 0 0;
}

.time-input-display {
    background: var(--bg-card);
    border: 2px solid var(--border-color);
    padding: 1rem;
    text-align: center;
    border-radius: 12px;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    box-shadow: inset 0 2px 4px var(--shadow-color);
    transition: all 0.3s ease;
}

.time-input-display:hover {
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.stNumberInput input, .stTextInput input {
    background-color: var(--button-bg) !important;
    border: 2px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    padding: 0.75rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

.stNumberInput input:focus, .stTextInput input:focus {
    border-color: var(--accent-color) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    outline: none !important;
}

.stSelectbox select {
    background-color: var(--button-bg) !important;
    border: 2px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    padding: 0.75rem !important;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
    }

    .hero-features {
        grid-template-columns: 1fr;
        gap: 1rem;
    }

    .feature-card {
        padding: 1.5rem;
    }

    .login-card {
        padding: 2rem;
        margin: 1rem;
    }

    .counter-card {
        padding: 1rem;
    }

    .counter-value {
        font-size: 2rem;
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.counter-card, .feature-card, .login-card {
    animation: fadeInUp 0.6s ease-out;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-color);
}
</style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "current_page" not in st.session_state:
    st.session_state.current_page = "hero"
if "result_days" not in st.session_state:
    st.session_state.result_days = 0
if "result_hours" not in st.session_state:
    st.session_state.result_hours = 0
if "result_minutes" not in st.session_state:
    st.session_state.result_minutes = 0
if "result_seconds" not in st.session_state:
    st.session_state.result_seconds = 0


def show_login():
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <h4 class="login-title">Let's count with</h4>
            <h1 class="login-title">LexCounter</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")

                login_clicked = st.form_submit_button("Sign In", use_container_width=True)

                if login_clicked:
                    if username and password:
                        users = load_users()
                        if username in users and verify_password(password, users[username]):
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.current_page = "hero"

                            if username not in st.session_state.data:
                                st.session_state.data[username] = {}
                                save_data(st.session_state.data)

                            st.success("Login successful!")
                            st.rerun()
                        else:
                            if username not in users:
                                users[username] = hash_password(password)
                                save_users(users)

                                if username not in st.session_state.data:
                                    st.session_state.data[username] = {}
                                    save_data(st.session_state.data)

                                st.session_state.authenticated = True
                                st.session_state.username = username
                                st.session_state.current_page = "hero"
                                st.success("Welcome! Account created and logged in!")
                                st.rerun()
                            else:
                                st.error("Invalid password")
                    else:
                        st.error("Please fill in all fields")


def show_hero():
    st.markdown(f"""
    <div class="user-bar">
        <div class="user-info">
            <span></span>
            <span>Welcome, <strong>{st.session_state.username}</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🚪 Logout", key="logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.current_page = "hero"
            st.rerun()

    # Clean title and subtitle without complex HTML
    st.markdown("Counter & Time Calculator")

    st.markdown("Choose Your Tool")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Open Counter", use_container_width=True, type="primary"):
            st.session_state.current_page = "counters"
            st.rerun()

    with col2:
        if st.button("Open Time Calculator", use_container_width=True, type="secondary"):
            st.session_state.current_page = "calculator"
            st.rerun()


def show_counters():
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("Home"):
            st.session_state.current_page = "hero"
            st.rerun()

    st.title("Counter Manager")
    st.subheader(f"User: {st.session_state.username}")

    counters = st.session_state.data.get(st.session_state.username, {})

    with st.form("add_counter", clear_on_submit=True):
        st.markdown("#### Add New Counter")
        new_counter = st.text_input("Counter name:", placeholder="Enter counter name...")
        if st.form_submit_button("➕ Add Counter", use_container_width=True):
            if new_counter and new_counter not in counters:
                counters[new_counter] = 0
                st.session_state.data[st.session_state.username] = counters
                save_data(st.session_state.data)
                st.success(f"Counter '{new_counter}' added successfully!")
                st.rerun()
            elif new_counter in counters:
                st.error("Counter already exists!")
            else:
                st.error("Enter a counter name")

    if counters:
        col1, col2 = st.columns([2, 1])
        with col1:
            sort_option = st.selectbox("Sort by:",
                                       ["Name (A→Z)", "Name (Z→A)", "Count (Low→High)", "Count (High→Low)"])

        with col2:
            if st.button("Delete All", type="primary"):
                st.session_state.data[st.session_state.username] = {}
                save_data(st.session_state.data)
                st.success("All counters deleted!")
                st.rerun()

        if sort_option == "Name (A→Z)":
            sorted_counters = sorted(counters.items())
        elif sort_option == "Name (Z→A)":
            sorted_counters = sorted(counters.items(), reverse=True)
        elif sort_option == "Count (Low→High)":
            sorted_counters = sorted(counters.items(), key=lambda x: x[1])
        else:
            sorted_counters = sorted(counters.items(), key=lambda x: x[1], reverse=True)

        for name, value in sorted_counters:
            st.markdown(f"""
            <div class="counter-card">
                <div class="counter-name">{name}</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="small")

            with col1:
                if st.button("Reset", key=f"reset_{name}", use_container_width=True):
                    counters[name] = 0
                    st.session_state.data[st.session_state.username] = counters
                    save_data(st.session_state.data)
                    st.rerun()

            with col2:
                if st.button("➖", key=f"dec_{name}", use_container_width=True):
                    counters[name] -= 1
                    st.session_state.data[st.session_state.username] = counters
                    save_data(st.session_state.data)
                    st.rerun()

            with col3:
                st.markdown(f'<div class="counter-value">{value}</div>', unsafe_allow_html=True)

            with col4:
                if st.button("➕", key=f"inc_{name}", use_container_width=True):
                    counters[name] += 1
                    st.session_state.data[st.session_state.username] = counters
                    save_data(st.session_state.data)
                    st.rerun()
    else:
        st.info("Create your first counter above!")


def show_time_calculator():
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("Home"):
            st.session_state.current_page = "hero"
            st.rerun()

    st.title("Time Calculator")
    st.subheader(f"User: {st.session_state.username}")

    st.markdown("This calculator can add or subtract two time values. Leave fields blank to use 0 as default.")

    st.markdown('<div class="time-calculator-container">', unsafe_allow_html=True)

    st.markdown("First Time Value")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.markdown("Days")
        day1 = st.number_input("", min_value=0, value=0, step=1, key="day1", label_visibility="collapsed")

    with col2:
        st.markdown("Hours")
        hour1 = st.number_input("", min_value=0, max_value=23, value=0, step=1, key="hour1",
                                label_visibility="collapsed")

    with col3:
        st.markdown("Minutes")
        minute1 = st.number_input("", min_value=0, max_value=59, value=0, step=1, key="minute1",
                                  label_visibility="collapsed")

    with col4:
        st.markdown("Seconds")
        second1 = st.number_input("", min_value=0, max_value=59, value=0, step=1, key="second1",
                                  label_visibility="collapsed")

    st.markdown("Operation")
    operation = st.radio("Choose operation:", ["➕ Add", "➖ Subtract"], horizontal=True)

    st.markdown("Second Time Value")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        day2 = st.number_input("", min_value=0, value=0, step=1, key="day2", label_visibility="collapsed")

    with col2:
        hour2 = st.number_input("", min_value=0, max_value=23, value=0, step=1, key="hour2",
                                label_visibility="collapsed")

    with col3:
        minute2 = st.number_input("", min_value=0, max_value=59, value=0, step=1, key="minute2",
                                  label_visibility="collapsed")

    with col4:
        second2 = st.number_input("", min_value=0, max_value=59, value=0, step=1, key="second2",
                                  label_visibility="collapsed")

    st.markdown("Result")
    st.markdown("<h2 style='text-align: center; margin: 20px 0; color: var(--text-primary);'>=</h2>",
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.markdown("Days")
        st.markdown(f'<div class="time-input-display">{st.session_state.result_days}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("Hours")
        st.markdown(f'<div class="time-input-display">{st.session_state.result_hours}</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("Minutes")
        st.markdown(f'<div class="time-input-display">{st.session_state.result_minutes}</div>', unsafe_allow_html=True)

    with col4:
        st.markdown("Seconds")
        st.markdown(f'<div class="time-input-display">{st.session_state.result_seconds}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("Calculate", use_container_width=True):
            total_seconds1 = day1 * 86400 + hour1 * 3600 + minute1 * 60 + second1
            total_seconds2 = day2 * 86400 + hour2 * 3600 + minute2 * 60 + second2

            if "Add" in operation:
                result_total_seconds = total_seconds1 + total_seconds2
            else:
                result_total_seconds = abs(total_seconds1 - total_seconds2)

            st.session_state.result_days = result_total_seconds // 86400
            remaining = result_total_seconds % 86400
            st.session_state.result_hours = remaining // 3600
            remaining = remaining % 3600
            st.session_state.result_minutes = remaining // 60
            st.session_state.result_seconds = remaining % 60

            st.success("Calculation completed!")
            st.rerun()

    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.result_days = 0
            st.session_state.result_hours = 0
            st.session_state.result_minutes = 0
            st.session_state.result_seconds = 0
            st.success("Results cleared!")
            st.rerun()


if not st.session_state.authenticated:
    show_login()
else:
    if st.session_state.current_page == "hero":
        show_hero()
    elif st.session_state.current_page == "counters":
        show_counters()
    elif st.session_state.current_page == "calculator":
        show_time_calculator()