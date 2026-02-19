"""Tests for Controller.google_controller."""
import pytest
from unittest.mock import MagicMock, patch


def test_init_oauth_registers_google():
    app = MagicMock()
    app.config = {"GOOGLE_CLIENT_ID": "cid", "GOOGLE_CLIENT_SECRET": "csec"}
    with patch("Controller.google_controller.oauth") as mock_oauth:
        from Controller.google_controller import init_oauth
        init_oauth(app)
        mock_oauth.init_app.assert_called_once_with(app)
        mock_oauth.register.assert_called_once()
        call_kw = mock_oauth.register.call_args[1]
        assert call_kw["client_id"] == "cid"
        assert call_kw["client_secret"] == "csec"
        assert "google" in str(mock_oauth.register.call_args).lower()
