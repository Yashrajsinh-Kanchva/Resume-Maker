"""Tests for Controller.page_controller."""
import pytest
from unittest.mock import patch
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    from Controller.page_controller import page_bp
    app.register_blueprint(page_bp)
    return app


def test_logout(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.get("/logout")
        assert rv.status_code in (302, 200)
        # Redirect to login
        assert "login" in rv.location.lower() or rv.status_code == 302


@patch("Controller.page_controller.send_from_directory")
def test_reset_password_page(mock_send, app):
    mock_send.return_value = "html content"
    with app.test_client() as client:
        rv = client.get("/reset-password/some-token")
        assert rv.status_code == 200
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        assert "reset-password" in args[1].lower()


@patch("Controller.page_controller.send_from_directory")
def test_forgot_password_page(mock_send, app):
    mock_send.return_value = "html content"
    with app.test_client() as client:
        rv = client.get("/forgot-password.html")
        assert rv.status_code == 200
        mock_send.assert_called_once()


@patch("Controller.page_controller.send_from_directory")
def test_terms_page(mock_send, app):
    mock_send.return_value = "html content"
    with app.test_client() as client:
        rv = client.get("/terms.html")
        assert rv.status_code == 200
        mock_send.assert_called_once()


def test_login_success_page_redirects_when_not_authenticated(app):
    with app.test_client() as client:
        rv = client.get("/login-success")
        assert rv.status_code == 302
        assert "login" in rv.location.lower()


def test_dashboard_redirects_when_not_authenticated(app):
    with app.test_client() as client:
        rv = client.get("/dashboard")
        assert rv.status_code == 302
        assert "login" in rv.location.lower()
