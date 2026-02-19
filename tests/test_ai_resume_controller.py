"""Tests for Controller.ai_resume_controller."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    from Controller.ai_resume_controller import ai_resume_bp
    app.register_blueprint(ai_resume_bp)
    return app


def test_suggest_resume_from_role_unauthorized(app):
    with app.test_client() as client:
        rv = client.post("/ai/suggest", json={"role": "Developer"})
        assert rv.status_code == 401
        assert "authenticated" in rv.get_json().get("error", "").lower()


def test_suggest_resume_from_role_missing_role(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.post("/ai/suggest", json={})
        assert rv.status_code == 400
        assert "role" in rv.get_json().get("error", "").lower()


@patch("Controller.ai_resume_controller.suggest_from_role")
def test_suggest_resume_from_role_success(mock_suggest, app):
    mock_suggest.return_value = {"title": "Dev", "summary": "S", "skills": [], "job_description": ""}
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.post("/ai/suggest", json={"role": "Developer"})
        assert rv.status_code == 200
        data = rv.get_json()
        assert data.get("title") == "Dev"
        mock_suggest.assert_called_once_with("Developer")


def test_create_resume_with_ai_unauthorized(app):
    with app.test_client() as client:
        rv = client.post("/ai/create-resume", json={})
        assert rv.status_code == 401


@patch("Controller.ai_resume_controller.create_ai_resume")
def test_create_resume_with_ai_success(mock_create, app):
    mock_create.return_value = "resume-id-123"
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.post("/ai/create-resume", json={"name": "Jane", "role": "Dev"})
        assert rv.status_code == 200
        data = rv.get_json()
        assert data.get("resumeId") == "resume-id-123"


def test_profile_status_no_session(app):
    with app.test_client() as client:
        rv = client.get("/api/profile/status")
        assert rv.status_code == 200
        data = rv.get_json()
        assert data.get("education") is False
        assert data.get("skills") is False


@patch("Controller.ai_resume_controller.user_repo")
def test_profile_status_with_user(mock_repo, app):
    mock_repo.find_user_by_email.return_value = {"education": "BS", "skills": ["Python"]}
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.get("/api/profile/status")
        assert rv.status_code == 200
        data = rv.get_json()
        assert data.get("education") is True
        assert data.get("skills") is True
