# Controller/Google.py
from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from utils.crypto_utils import CryptoUtils
import os
import secrets


from services.user_service import UserService

# ✅ ADD url_prefix
google_bp = Blueprint(
    "google",
    __name__,
    url_prefix="/api/auth/google"
)

oauth = OAuth()
user_service = UserService()


def init_oauth(app):
    oauth.init_app(app)
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    if client_id and client_secret:
        oauth.register(
            name="google",
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )

# ✅ FINAL LOGIN URL
@google_bp.route("/login", methods=["GET"])
def google_login():
    nonce = secrets.token_urlsafe(16)
    session["google_nonce"] = nonce

    redirect_uri = url_for("google.google_callback", _external=True)
    return oauth.google.authorize_redirect(
        redirect_uri=redirect_uri,
        nonce=nonce
    )

@google_bp.route("/callback", methods=["GET"])
def google_callback():
    nonce = session.pop("google_nonce", None)

    token = oauth.google.authorize_access_token()
    profile = oauth.google.parse_id_token(token, nonce=nonce)

    result = user_service.login_with_google(profile)

    if not result["success"]:
        session.pop("user", None)
        return redirect(f"/login?error={result['message']}")

    user = result["user"]

    session["user"] = {
        "email": user["email"],
        "name": user["name"],
        "provider": "google",
        "role": user.get("role", "user")
    }

    return redirect("/login-success")
