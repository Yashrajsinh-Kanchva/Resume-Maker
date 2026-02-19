from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

google_bp = Blueprint("google_auth", __name__, url_prefix="/api/auth")
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )


# ================= GOOGLE LOGIN =================
@google_bp.route("/google/login", methods=["GET"])
def google_login():
    # Explicitly construct redirect URI to match Google Cloud configuration
    # Use 127.0.0.1 instead of localhost to avoid mismatch
    redirect_uri = "http://127.0.0.1:5000/api/auth/google/callback"
    return oauth.google.authorize_redirect(redirect_uri)


# ================= GOOGLE CALLBACK =================
@google_bp.route("/google/callback", methods=["GET"])
def google_callback():
    oauth.google.authorize_access_token()
    user_info = oauth.google.get("userinfo").json()

    session["user"] = {
        "email": user_info["email"],
        "name": user_info["name"],
        "picture": user_info.get("picture")
    }

    return redirect("/dashboard")
