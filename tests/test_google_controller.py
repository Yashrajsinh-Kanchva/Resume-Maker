"""Tests for Controller.Google (Google OAuth)."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


def test_init_oauth_registers_when_creds_present():
    app = MagicMock()
    app.config = {}
    with patch.dict("os.environ", {"GOOGLE_CLIENT_ID": "cid", "GOOGLE_CLIENT_SECRET": "csec"}):
        with patch("Controller.Google.oauth") as mock_oauth:
            from Controller.Google import init_oauth
            init_oauth(app)
            mock_oauth.init_app.assert_called_once_with(app)
            mock_oauth.register.assert_called_once()
            kwargs = mock_oauth.register.call_args[1]
            assert kwargs["client_id"] == "cid"
            assert kwargs["client_secret"] == "csec"


def test_init_oauth_skips_register_when_no_creds():
    app = MagicMock()
    app.config = {}
    with patch.dict("os.environ", {}, clear=True):
        with patch("Controller.Google.oauth") as mock_oauth:
            from Controller.Google import init_oauth
            init_oauth(app)
            mock_oauth.init_app.assert_called_once()
            mock_oauth.register.assert_not_called()


@patch("Controller.Google.oauth")
def test_google_login_sets_nonce_and_redirects(mock_oauth):
    from flask import redirect
    mock_oauth.google.authorize_redirect.return_value = redirect("https://accounts.google.com")
    app = Flask(__name__)
    app.secret_key = "test-secret"
    from Controller.Google import google_bp
    app.register_blueprint(google_bp)
    with app.test_client() as client:
        rv = client.get("/api/auth/google/login")
        assert rv.status_code in (302, 200)
        with client.session_transaction() as sess:
            assert "google_nonce" in sess
