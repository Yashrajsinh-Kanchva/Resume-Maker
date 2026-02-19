"""Tests for Controller.contact_email_controller."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    from Controller.contact_email_controller import contact_api
    app.register_blueprint(contact_api)
    return app


def test_send_contact_email_missing_fields(app):
    with app.test_client() as client:
        rv = client.post("/api/contact/send", json={})
        assert rv.status_code == 400
        data = rv.get_json()
        assert "required" in data.get("msg", "").lower() or "fields" in data.get("msg", "").lower()


def test_send_contact_email_partial_fields(app):
    with app.test_client() as client:
        rv = client.post("/api/contact/send", json={"name": "A", "email": "a@gmail.com"})
        assert rv.status_code == 400


@patch("Controller.contact_email_controller.smtplib.SMTP")
def test_send_contact_email_success(mock_smtp, app):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server
    with app.test_client() as client:
        rv = client.post("/api/contact/send", json={
            "name": "Jane", "email": "j@gmail.com",
            "subject": "Help", "message": "I need help"
        })
        assert rv.status_code == 200
        data = rv.get_json()
        assert data.get("success") is True
        assert "sent" in data.get("msg", "").lower() or "success" in data.get("msg", "").lower()
