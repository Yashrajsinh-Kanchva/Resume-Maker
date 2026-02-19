"""Tests for api.admin.chatbot."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


def test_respond():
    from flask import Flask
    from api.admin.chatbot import _respond
    app = Flask(__name__)
    with app.app_context():
        resp, status = _respond("Hello")
        assert status == 200
        assert resp.headers.get("X-Chatbot-Build")
        assert resp.headers.get("X-Chatbot-Mode") == "rule"


def test_sanitize():
    from api.admin.chatbot import _sanitize
    assert _sanitize("  How many users?  ") == "how many users?"
    assert _sanitize("") == ""
    assert _sanitize(None) == ""


def test_extract_feedback_name():
    from api.admin.chatbot import _extract_feedback_name
    assert "mihir" in _extract_feedback_name("feedback where name is mihir").lower()
    assert _extract_feedback_name("how many users") == ""


def test_asks_how_many():
    from api.admin.chatbot import _asks_how_many
    assert _asks_how_many("how many users") is True
    assert _asks_how_many("total users") is False


def test_asks_total():
    from api.admin.chatbot import _asks_total
    assert _asks_total("total users") is True
    assert _asks_total("count resumes") is True


def test_has_feedback():
    from api.admin.chatbot import _has_feedback
    assert _has_feedback("how many feedback") is True
    assert _has_feedback("feedback by john") is True


def test_has_user():
    from api.admin.chatbot import _has_user
    assert _has_user("how many users") is True


def test_has_resume():
    from api.admin.chatbot import _has_resume
    assert _has_resume("how many resumes") is True
    assert _has_resume("total cv") is True


@patch("api.admin.chatbot.db")
def test_rule_total_users(mock_db):
    mock_db.__getitem__.return_value.count_documents.return_value = 10
    from api.admin.chatbot import _rule_total_users
    result = _rule_total_users("how many users")
    assert "10" in result
    assert "user" in result.lower()


@patch("api.admin.chatbot.db")
def test_rule_total_resumes(mock_db):
    mock_db.__getitem__.return_value.count_documents.return_value = 5
    from api.admin.chatbot import _rule_total_resumes
    result = _rule_total_resumes("how many resumes")
    assert "5" in result
    assert "resume" in result.lower()


@pytest.fixture
def app():
    app = Flask(__name__)
    from api.admin.chatbot import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix="/api/admin")
    return app


def test_chatbot_missing_auth(app):
    with app.test_client() as client:
        rv = client.post("/api/admin/chatbot", json={"question": "how many users"})
        assert rv.status_code == 401
        assert "authorization" in rv.get_json().get("answer", "").lower() or "required" in rv.get_json().get("answer", "").lower()


def test_chatbot_empty_question(app):
    with app.test_client() as client:
        with patch("api.admin.chatbot._admin_service") as mock_svc:
            mock_svc.is_admin.return_value = True
            rv = client.post(
                "/api/admin/chatbot",
                json={"question": ""},
                headers={"X-Admin-Email": "admin@gmail.com"}
            )
        assert rv.status_code == 400


@patch("api.admin.chatbot._match_rule")
@patch("api.admin.chatbot._admin_service")
def test_chatbot_success_rule(mock_svc, mock_rule, app):
    mock_svc.is_admin.return_value = True
    mock_rule.return_value = "There are 5 users."
    with app.test_client() as client:
        rv = client.post(
            "/api/admin/chatbot",
            json={"question": "how many users"},
            headers={"X-Admin-Email": "admin@gmail.com"}
        )
    assert rv.status_code == 200
    data = rv.get_json()
    assert "answer" in data
    assert "5" in data["answer"]
