"""Tests for Controller.google_controller (OAuth)."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, redirect


def test_init_oauth():
    app = MagicMock()
    app.config = {}
    with patch.dict("os.environ", {"GOOGLE_CLIENT_ID": "cid", "GOOGLE_CLIENT_SECRET": "csec"}):
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
    kwargs = mock_oauth.google.authorize_redirect.call_args[1]
    redirect_uri = kwargs.get("redirect_uri", "")
    assert "callback" in redirect_uri and ("127.0.0.1" in redirect_uri or "localhost" in redirect_uri)


@patch("Controller.google_controller.user_service")
@patch("Controller.google_controller.oauth")
def test_google_callback_sets_session_and_redirects(mock_oauth, mock_user_svc):
    mock_oauth.google.authorize_access_token.return_value = None
    mock_oauth.google.parse_id_token.return_value = {"email": "u@gmail.com", "name": "User"}
    mock_user_svc.login_with_google.return_value = {
        "success": True,
        "user": {"email": "u@gmail.com", "name": "User", "role": "user"}
    }
    app = Flask(__name__)
    app.secret_key = "secret"
    from Controller.google_controller import google_bp
    app.register_blueprint(google_bp)
    with app.test_client() as client:
        rv = client.get("/api/auth/google/callback")
    assert rv.status_code == 302
    assert "login-success" in rv.location
    with client.session_transaction() as sess:
        user = sess.get("user", {})
        assert user.get("email") == "u@gmail.com"
        assert user.get("name") == "User"
        assert user.get("provider") == "google"
        assert user.get("role") == "user"
