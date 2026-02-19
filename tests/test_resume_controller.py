"""Tests for Controller.resume_controller."""
import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    from Controller.resume_controller import resume_bp
    app.register_blueprint(resume_bp)
    return app


def test_is_valid_resume_id():
    from Controller.resume_controller import _is_valid_resume_id
    assert _is_valid_resume_id(str(ObjectId())) is True
    assert _is_valid_resume_id("invalid") is False
    assert _is_valid_resume_id("") is False
    assert _is_valid_resume_id(None) is False
    assert _is_valid_resume_id(123) is False


def test_create_resume_unauthorized(app):
    with app.test_client() as client:
        rv = client.post("/", json={"data": {}})
        assert rv.status_code == 401
        assert rv.get_json().get("message") == "Unauthorized"


@patch("Controller.resume_controller.resume_service")
def test_create_resume_authenticated(mock_svc, app):
    mock_svc.create_resume.return_value = {"success": True, "message": "Resume saved"}
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.post("/", json={"data": {"step1": {}}})
        assert rv.status_code == 200
        assert rv.get_json().get("success") is True
        mock_svc.create_resume.assert_called_once()


def test_get_resumes_unauthorized(app):
    with app.test_client() as client:
        rv = client.get("/")
        assert rv.status_code == 401
        assert rv.get_json() == []


@patch("Controller.resume_controller.rank_resumes")
@patch("Controller.resume_controller.resume_service")
def test_get_resumes_authenticated(mock_svc, mock_rank, app):
    mock_svc.get_user_resumes.return_value = []
    mock_rank.return_value = []
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.get("/")
        assert rv.status_code == 200
        assert rv.get_json() == []
        mock_rank.assert_called_once()


def test_get_single_resume_unauthorized(app):
    with app.test_client() as client:
        rv = client.get("/" + str(ObjectId()))
        assert rv.status_code == 401


def test_get_single_resume_invalid_id(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.get("/invalid-id")
        assert rv.status_code in (400, 404)


@patch("Controller.resume_controller.resume_service")
def test_get_single_resume_not_found(mock_svc, app):
    mock_svc.get_resume_by_id.return_value = None
    oid = str(ObjectId())
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.get("/" + oid)
        assert rv.status_code == 404
        mock_svc.get_resume_by_id.assert_called_once()
