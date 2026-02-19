"""Tests for Controller.chat_controller."""
import pytest
from unittest.mock import patch
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    from Controller.chat_controller import chat_api
    app.register_blueprint(chat_api)
    return app


def test_get_client_id_from_forwarded():
    from Controller.chat_controller import get_client_id
    req = type("Req", (), {"headers": {"X-Forwarded-For": "1.2.3.4, 5.6.7.8"}, "remote_addr": None})()
    assert get_client_id(req) == "1.2.3.4"


def test_get_client_id_local():
    from Controller.chat_controller import get_client_id
    req = type("Req", (), {"headers": {}, "remote_addr": "127.0.0.1"})()
    assert get_client_id(req) == "local"


@patch("Controller.chat_controller.is_rate_limited", return_value=True)
@patch("Controller.chat_controller.process_chat")
def test_chat_rate_limited(mock_process, mock_limited, app):
    with app.test_client() as client:
        rv = client.post("/", json={"message": "hello"})
        assert rv.status_code == 429
        data = rv.get_json()
        assert data.get("intent") == "RATE_LIMIT"
        mock_process.assert_not_called()


@patch("Controller.chat_controller.is_rate_limited", return_value=False)
@patch("Controller.chat_controller.process_chat", return_value=("Reply here", "GO_TO_CONTACT"))
def test_chat_success(mock_process, mock_limited, app):
    with app.test_client() as client:
        rv = client.post("/", json={"message": "how to download resume"})
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["reply"] == "Reply here"
        assert data["intent"] == "GO_TO_CONTACT"
        mock_process.assert_called_once_with("how to download resume")
