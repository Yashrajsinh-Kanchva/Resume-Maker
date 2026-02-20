import streamlit as st
import requests

# Importing Modular Sections for Admin Panel

from sections.dashboard import dashboard_page
from sections.users import users_page
from sections.resumes import resumes_page
from sections.system import system_page
from sections.logs import logs_page
from sections.analytics import analytics_page
from sections.chatbot import chatbot_page

# ---------------- CONFIG ----------------

API_BASE = "http://127.0.0.1:5000/api/admin"

st.set_page_config(
    page_title="Resume Maker | Admin",
    page_icon="🛠️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "admin" not in st.session_state or st.session_state.admin is None:
    st.session_state.admin = None


# ---------------- LOGIN SCREEN ----------------

def login_screen():
    st.title("🔐 Admin Login")

    with st.form("admin_login_form"):
        email = st.text_input("Admin Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if not submit:
        return

    if not email or not password:
        st.warning("Email and password are required")
        return

    try:
        res = requests.post(
            f"{API_BASE}/login",
            json={"email": email, "password": password},
            timeout=5
        )

        if res.status_code != 200:
            try:
                st.error(res.json().get("message", "Login failed"))
            except Exception:
                st.error("Login failed")
            return

        data = res.json()

        if data.get("success") and data.get("admin"):
            st.session_state.admin = data["admin"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error(data.get("message", "Invalid credentials"))

    except requests.exceptions.RequestException:
        st.error("Backend server not reachable")


# ---------------- AUTH GATE ----------------

if not st.session_state.admin:
    login_screen()
    st.stop()


# ---------------- SIDEBAR ----------------

admin = st.session_state.get("admin", {})
admin_name = admin.get("name", "Admin")

st.sidebar.title("🛠️ Admin Panel")
st.sidebar.write(f"👤 **{admin_name}**")

if st.sidebar.button("🚪 Logout"):
    st.session_state.admin = None
    st.rerun()

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Users", "Resumes", "Analytics", "Chatbot", "System", "Logs"]
)

# ---------------- ROUTING ----------------

if menu == "Dashboard":
    dashboard_page(API_BASE)

elif menu == "Users":
    users_page(API_BASE)

elif menu == "Resumes":
    resumes_page(API_BASE)

elif menu == "Analytics":
    analytics_page(API_BASE)

elif menu == "Chatbot":
    chatbot_page(API_BASE)

elif menu == "System":
    system_page(API_BASE)

elif menu == "Logs":
    logs_page(API_BASE)
