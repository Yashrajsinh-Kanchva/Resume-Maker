"""Tests for Controller.admin_controller."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    from Controller.admin_controller import admin_bp
    app.register_blueprint(admin_bp)
    return app


def test_resolve_log_path():
    from Controller.admin_controller import _resolve_log_path
    assert _resolve_log_path("admin") is not None
    assert _resolve_log_path("service") is not None
    assert _resolve_log_path("ats_controller") is not None
    assert _resolve_log_path("ats_checker") is not None
    assert _resolve_log_path("invalid") is None


@patch("Controller.admin_controller.resume_service")
def test_get_all_resumes_admin(mock_svc, app):
    mock_svc.get_all_resumes_for_admin.return_value = []
    with app.test_client() as client:
        rv = client.get("/api/admin/resumes")
        assert rv.status_code == 200
        data = rv.get_json()
        assert data.get("success") is True
        assert "data" in data


@patch("Controller.admin_controller.analytics_service")
def test_get_analytics(mock_svc, app):
    mock_svc.get_analytics.return_value = {
        "users_over_time": [], "resumes_over_time": [], "top_users": []
    }
    with app.test_client() as client:
        rv = client.get("/api/admin/analytics")
        assert rv.status_code == 200
        data = rv.get_json()
        assert "users_over_time" in data or "top_users" in data


@patch("Controller.admin_controller.admin_service")
def test_get_users(mock_svc, app):
    mock_svc.get_all_users.return_value = [{"email": "a", "name": "A"}]
    with app.test_client() as client:
        rv = client.get("/api/admin/users")
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)


def test_admin_login_missing_fields(app):
    with app.test_client() as client:
        rv = client.post("/api/admin/login", json={})
        assert rv.status_code == 400
        assert "required" in rv.get_json().get("message", "").lower()


def test_admin_login_invalid_email(app):
    with app.test_client() as client:
        rv = client.post("/api/admin/login", json={"email": "x@yahoo.com", "password": "p"})
        assert rv.status_code == 400
        assert "invalid" in rv.get_json().get("message", "").lower()


@patch("Controller.admin_controller.admin_service")
def test_admin_login_success(mock_svc, app):
    mock_svc.login_admin.return_value = {"success": True}
    with app.test_client() as client:
        rv = client.post("/api/admin/login", json={"email": "admin@gmail.com", "password": "pass"})
        assert rv.status_code == 200


@patch("Controller.admin_controller.admin_service")
def test_block_user(mock_svc, app):
    with app.test_client() as client:
        rv = client.post("/api/admin/users/block", json={"email": "u@gmail.com"})
        assert rv.status_code == 200
        mock_svc.block_user.assert_called_once_with("u@gmail.com")


@patch("Controller.admin_controller.admin_service")
def test_export_users_csv(mock_svc, app):
    mock_svc.get_all_users.return_value = [{"email": "e", "name": "N", "provider": "local", "status": "active", "role": "user"}]
    with app.test_client() as client:
        rv = client.get("/api/admin/users/export")
        assert rv.status_code == 200
        assert "text/csv" in rv.content_type
        assert b"Email" in rv.data


@patch("Controller.admin_controller.resume_service")
def test_export_resumes_csv(mock_svc, app):
    mock_svc.get_all_resumes_for_admin.return_value = [{"email": "e", "title": "T", "created_at": ""}]
    with app.test_client() as client:
        rv = client.get("/api/admin/resumes/export")
        assert rv.status_code == 200
        assert "text/csv" in rv.content_type


def test_get_logs_invalid_type(app):
    with app.test_client() as client:
        rv = client.get("/api/admin/logs?type=invalid_type")
        assert rv.status_code == 400
        assert "invalid" in rv.get_json().get("message", "").lower()
