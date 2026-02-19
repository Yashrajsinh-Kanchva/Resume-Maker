"""Tests for Controller.feedback_controller."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    from Controller.feedback_controller import feedback_bp
    app.register_blueprint(feedback_bp)
    return app


def test_save_feedback_missing_fields(app):
    with app.test_client() as client:
        rv = client.post("/api/feedback", json={})
        assert rv.status_code == 400
        assert "required" in rv.get_json().get("msg", "").lower()


def test_save_feedback_partial_fields(app):
    with app.test_client() as client:
        rv = client.post("/api/feedback", json={"name": "A", "email": "a@gmail.com"})
        assert rv.status_code == 400


@patch("Controller.feedback_controller.get_feedback_collection")
def test_save_feedback_success(mock_get_coll, app):
    mock_coll = MagicMock()
    mock_get_coll.return_value = mock_coll
    with app.test_client() as client:
        rv = client.post("/api/feedback", json={
            "name": "Jane", "email": "j@gmail.com", "rating": 5, "message": "Great app!"
        })
        assert rv.status_code == 201
        assert rv.get_json().get("msg") == "Feedback saved successfully"
        mock_coll.insert_one.assert_called_once()
        call_arg = mock_coll.insert_one.call_args[0][0]
        assert call_arg["name"] == "Jane"
        assert call_arg["rating"] == 5


@patch("Controller.feedback_controller.get_feedback_collection")
def test_get_feedbacks(mock_get_coll, app):
    mock_coll = MagicMock()
    chain = MagicMock()
    chain.limit.return_value = [{"name": "A", "feedback": "Good"}]
    mock_coll.find.return_value.sort.return_value = chain
    mock_get_coll.return_value = mock_coll
    with app.test_client() as client:
        rv = client.get("/api/feedbacks")
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "A"
