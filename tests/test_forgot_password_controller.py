"""Tests for Controller.forgot_password_controller."""
import pytest
from unittest.mock import patch
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    app.config["MAIL_USERNAME"] = "noreply@test.com"
    from Controller.forgot_password_controller import forgot_password_bp
    app.register_blueprint(forgot_password_bp)
    return app


@patch("Controller.forgot_password_controller.mail")
def test_forgot_password_success(mock_mail, app):
    with app.test_client() as client:
        rv = client.post("/forgot-password", data={"email": "user@gmail.com"})
        assert rv.status_code == 200
        assert "reset" in rv.data.decode().lower() or "sent" in rv.data.decode().lower()
        mock_mail.send.assert_called_once()
