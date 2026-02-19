"""Tests for Controller.google_controller (OAuth)."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, redirect


def test_init_oauth():
    app = MagicMock()
    app.config = {"GOOGLE_CLIENT_ID": "cid", "GOOGLE_CLIENT_SECRET": "csec"}
    with patch("Controller.google_controller.oauth") as mock_oauth:
        from Controller.google_controller import init_oauth
        init_oauth(app)
        mock_oauth.init_app.assert_called_once_with(app)
        mock_oauth.register.assert_called_once()
        assert mock_oauth.register.call_args[1]["client_id"] == "cid"


@patch("Controller.google_controller.oauth")
def test_google_login_redirects(mock_oauth):
    mock_oauth.google.authorize_redirect.return_value = redirect("https://accounts.google.com")
    app = Flask(__name__)
    app.secret_key = "test"
    from Controller.google_controller import google_bp
    app.register_blueprint(google_bp)
    with app.test_client() as client:
        rv = client.get("/api/auth/google/login")
    assert rv.status_code in (302, 200)
    mock_oauth.google.authorize_redirect.assert_called_once()
    (redirect_uri,) = mock_oauth.google.authorize_redirect.call_args[0]
    assert "127.0.0.1" in redirect_uri and "callback" in redirect_uri


@patch("Controller.google_controller.oauth")
def test_google_callback_sets_session_and_redirects(mock_oauth):
    mock_oauth.google.authorize_access_token.return_value = None
    mock_oauth.google.get.return_value.json.return_value = {
        "email": "u@gmail.com", "name": "User", "picture": "https://photo"
    }
    app = Flask(__name__)
    app.secret_key = "secret"
    from Controller.google_controller import google_bp
    app.register_blueprint(google_bp)
    with app.test_client() as client:
        rv = client.get("/api/auth/google/callback")
    assert rv.status_code == 302
    assert "dashboard" in rv.location
    with client.session_transaction() as sess:
        assert sess.get("user", {}).get("email") == "u@gmail.com"
        assert sess.get("user", {}).get("name") == "User"
