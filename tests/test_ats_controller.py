"""Tests for Controller.ats_controller."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    from Controller.ats_controller import ats_bp
    app.register_blueprint(ats_bp)
    return app


def test_allowed_file():
    from Controller.ats_controller import allowed_file
    assert allowed_file("resume.pdf") is True
    assert allowed_file("resume.PDF") is True
    assert allowed_file("doc.docx") is False
    assert allowed_file("noext") is False


def test_check_resume_no_file(app):
    with app.test_client() as client:
        rv = client.post("/api/ats/check", data={})
        assert rv.status_code == 400
        data = rv.get_json()
        assert "no resume" in data.get("error", "").lower() or "file" in data.get("error", "").lower()


def test_check_resume_empty_filename(app):
    from io import BytesIO
    with app.test_client() as client:
        rv = client.post("/api/ats/check", data={
            "resume": (BytesIO(b""), ""),
            "job_description": "JD here"
        })
        assert rv.status_code == 400
        assert "file" in rv.get_json().get("error", "").lower() or "selected" in rv.get_json().get("error", "").lower()


def test_check_resume_invalid_file_type(app):
    from io import BytesIO
    with app.test_client() as client:
        rv = client.post("/api/ats/check", data={
            "resume": (BytesIO(b""), "image.png"),
            "job_description": "JD"
        })
        assert rv.status_code == 400
        data = rv.get_json()
        assert "pdf" in data.get("error", "").lower() or "invalid" in data.get("error", "").lower()


def test_check_resume_no_job_description(app):
    from io import BytesIO
    with app.test_client() as client:
        rv = client.post("/api/ats/check", data={
            "resume": (BytesIO(b"pdf content"), "resume.pdf"),
        })
        assert rv.status_code == 400
        data = rv.get_json()
        assert "job" in data.get("error", "").lower() or "description" in data.get("error", "").lower()


def test_check_resume_from_saved_unauthorized(app):
    with app.test_client() as client:
        rv = client.post("/api/ats/check-from-resume", json={"resume_id": "x", "job_description": "JD"})
        assert rv.status_code == 401


def test_check_resume_from_saved_no_body(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.post("/api/ats/check-from-resume", json={})
        assert rv.status_code == 400
        assert "required" in rv.get_json().get("error", "").lower() or "body" in rv.get_json().get("error", "").lower()


def test_check_resume_from_saved_missing_resume_id(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.post("/api/ats/check-from-resume", json={"job_description": "JD"})
        assert rv.status_code == 400
        assert "resume_id" in rv.get_json().get("error", "").lower()


def test_check_resume_from_saved_missing_job_description(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.post("/api/ats/check-from-resume", json={"resume_id": "507f1f77bcf86cd799439011"})
        assert rv.status_code == 400


@patch("Controller.ats_controller.resume_service")
@patch("Controller.ats_controller.ats_service")
def test_check_resume_from_saved_resume_not_found(mock_ats, mock_resume, app):
    mock_resume.get_resume_by_id.return_value = None
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.post("/api/ats/check-from-resume", json={
            "resume_id": "507f1f77bcf86cd799439011",
            "job_description": "Job description here"
        })
        assert rv.status_code == 404
        assert "not found" in rv.get_json().get("error", "").lower()
