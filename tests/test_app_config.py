"""Tests for config.app_config."""
import pytest
from config.app_config import BASE_DIR, FSD_DIR, HTML_DIR, CSS_DIR, JS_DIR, IMG_DIR, Config


class TestAppConfigPaths:
    def test_base_dir_absolute(self):
        assert len(BASE_DIR) > 0
        # Absolute path (Unix / or Windows C:)
        assert BASE_DIR.startswith("/") or (len(BASE_DIR) >= 2 and BASE_DIR[1] == ":") or "Python" in BASE_DIR

    def test_fsd_dir_contains_fsd(self):
        assert "FSD" in FSD_DIR

    def test_html_dir_contains_html(self):
        assert "HTML" in HTML_DIR

    def test_css_js_img_dirs_defined(self):
        assert "CSS" in CSS_DIR
        assert "JS" in JS_DIR
        assert "IMG" in IMG_DIR


class TestConfig:
    def test_secret_key_default(self):
        assert hasattr(Config, "SECRET_KEY")
        assert Config.SECRET_KEY is not None

    def test_session_cookie_httponly(self):
        assert Config.SESSION_COOKIE_HTTPONLY is True

    def test_session_cookie_samesite(self):
        assert Config.SESSION_COOKIE_SAMESITE == "Lax"
