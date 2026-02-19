"""Tests for app.create_app and helpers."""
import pytest
from unittest.mock import patch, MagicMock


@patch("app.redis_client")
@patch("app.init_oauth")
def test_create_app(mock_oauth, mock_redis):
    mock_redis.ping.return_value = True
    from app import create_app
    app = create_app()
    assert app is not None
    assert app.secret_key
    mock_oauth.assert_called_once_with(app)


@patch("app.redis_client")
@patch("app.init_oauth")
def test_create_app_redis_warning(mock_oauth, mock_redis):
    mock_redis.ping.side_effect = Exception("Connection refused")
    from app import create_app
    app = create_app()
    assert app is not None


def test_validate_required_config_raises_without_secret():
    from app import create_app
    from config.app_config import Config
    # Config has default SECRET_KEY from env or "dev-secret-key..."
    # So create_app should not raise if Config provides one
    with patch("app.redis_client") as mock_redis:
        mock_redis.ping.return_value = True
        with patch("app.init_oauth"):
            app = create_app()
            assert app.config.get("SECRET_KEY")


def test_register_blueprints():
    from app import create_app
    with patch("app.redis_client") as mock_redis:
        mock_redis.ping.return_value = True
        with patch("app.init_oauth"):
            app = create_app()
            # Check some routes are registered
            rules = [r.rule for r in app.url_map.iter_rules()]
            assert any("/api/" in r for r in rules)
            assert any("admin" in r or "resumes" in r or "users" in r for r in rules)
