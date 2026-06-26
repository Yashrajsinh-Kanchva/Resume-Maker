from flask import Blueprint, request, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from utils.mail_utils import mail



forgot_password_bp = Blueprint("forgot_password_bp", __name__)

@forgot_password_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    email = request.form.get("email")

    serializer = URLSafeTimedSerializer(current_app.secret_key)
    token = serializer.dumps(email, salt="password-reset")

    reset_link = f"/reset-password/{token}"

    msg = Message(
        subject="Reset Your Resume Maker Password",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = f"""
Click the link below to reset your password:

{reset_link}

This link is valid for 1 hour.
"""

    mail.send(msg)
    return "Reset password link sent successfully"
