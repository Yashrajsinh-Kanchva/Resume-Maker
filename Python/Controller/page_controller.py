from flask import Blueprint, send_from_directory, session, redirect, url_for
from config.app_config import HTML_DIR

page_bp = Blueprint("pages", __name__)
LOGIN_PAGE_ENDPOINT = "pages.login_page"

# ---------------- LANDING PAGE ----------------
@page_bp.route("/", methods=["GET"])
def landing_page():
    return send_from_directory(HTML_DIR, "landing page.html")

# ---------------- LOGIN ----------------
@page_bp.route("/login", methods=["GET"])
@page_bp.route("/loginPage.html", methods=["GET"])
def login_page():
    return send_from_directory(HTML_DIR, "loginPage.html")


# ---------------- SIGNUP ----------------
@page_bp.route("/signUp.html", methods=["GET"])
def signup_page():
    return send_from_directory(HTML_DIR, "signUp.html")


# ---------------- LOGIN SUCCESS ----------------
@page_bp.route("/login-success", methods=["GET"])
@page_bp.route("/login-success.html", methods=["GET"])
def login_success_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "login-success.html")


# ---------------- DASHBOARD ----------------
@page_bp.route("/dashboard", methods=["GET"])
@page_bp.route("/dashboard.html", methods=["GET"])
def dashboard_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "dashboard.html")


# ---------------- CONTACT ----------------
@page_bp.route("/contact.html", methods=["GET"])
def contact_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "contact.html")


# ---------------- SETTINGS ----------------
@page_bp.route("/settings.html", methods=["GET"])
def settings_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "settings.html")


# ---------------- DOCUMENTS ----------------
@page_bp.route("/documents.html", methods=["GET"])
def documents_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "documents.html")


# ---------------- LOGOUT ----------------
@page_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for(LOGIN_PAGE_ENDPOINT))

# ---------------- RESET PASSWORD ----------------
@page_bp.route("/reset-password/<token>", methods=["GET"])
def reset_password_page(token):
    return send_from_directory(
        HTML_DIR,
        "reset-password.html"
    )

@page_bp.route("/terms.html", methods=["GET"])
def terms_page():
    return send_from_directory(HTML_DIR, "terms.html")

# ---------------- FORGOT PASSWORD PAGE ----------------
@page_bp.route("/forgot-password.html", methods=["GET"])
def forgot_password_page():
    return send_from_directory(HTML_DIR, "forgot-password.html")


# ---------------- CHOOSE TEMPLATE ----------------
@page_bp.route("/choose-template.html", methods=["GET"])
def choose_template_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "choose-template.html")

# ---------------- STEP 1 ----------------
@page_bp.route("/step-1.html", methods=["GET"])
def step_1_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "step-1.html")


# ---------------- STEP 2 ----------------
@page_bp.route("/step-2.html", methods=["GET"])
def step_2_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "step-2.html")


# ---------------- STEP 3 ----------------
@page_bp.route("/step-3.html", methods=["GET"])
def step_3_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "step-3.html")


# ---------------- STEP 4 ----------------
@page_bp.route("/step-4.html", methods=["GET"])
def step_4_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "step-4.html")

# ---------------- BUILD RESUME ----------------
@page_bp.route("/build-resume.html", methods=["GET"])
def build_resume_page():
    if "user" not in session:
        return redirect(url_for(LOGIN_PAGE_ENDPOINT))
    return send_from_directory(HTML_DIR, "build-resume.html")

@page_bp.route("/navbar.html", methods=["GET"])
def navbar_file():
    return send_from_directory(HTML_DIR, "navbar.html")

@page_bp.route("/feedback.html", methods=["GET"])
def feedback():
    return send_from_directory(HTML_DIR,"feedback.html")

@page_bp.route("/about.html", methods=["GET"])
def about_page():
    return send_from_directory(HTML_DIR, "about.html")
