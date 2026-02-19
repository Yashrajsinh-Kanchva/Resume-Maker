"""Tests for Controller.user_controller."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    from Controller.user_controller import user_bp
    app.register_blueprint(user_bp)
    return app


def test_hc(app):
    with app.test_client() as client:
        rv = client.get("/hc")
        assert rv.status_code == 200
        assert rv.data.decode() == "done"


def test_get_me_unauthorized(app):
    with app.test_client() as client:
        rv = client.get("/me")
        assert rv.status_code == 401
        data = rv.get_json()
        assert data.get("authenticated") is False


def test_get_me_authenticated(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com", "name": "U"}
        rv = client.get("/me")
        assert rv.status_code == 200
        data = rv.get_json()
        assert data.get("authenticated") is True
        assert data["user"]["email"] == "u@gmail.com"


def test_signup_missing_fields(app):
    with app.test_client() as client:
        rv = client.post("/signup", data={})
        assert rv.status_code == 400
        assert "required" in rv.get_json().get("message", "").lower()


def test_signup_invalid_email(app):
    with app.test_client() as client:
        rv = client.post("/signup", data={
            "name": "A", "email": "user@yahoo.com", "password": "Pass1@word", "confirm_password": "Pass1@word"
        })
        assert rv.status_code == 400
        assert "gmail" in rv.get_json().get("message", "").lower()


def test_signup_password_mismatch(app):
    with app.test_client() as client:
        rv = client.post("/signup", data={
            "name": "A", "email": "a@gmail.com", "password": "Pass1@word", "confirm_password": "Other1@word"
        })
        assert rv.status_code == 400
        assert "match" in rv.get_json().get("message", "").lower()


def test_signup_invalid_password_format(app):
    with app.test_client() as client:
        rv = client.post("/signup", data={
            "name": "A", "email": "a@gmail.com", "password": "short", "confirm_password": "short"
        })
        assert rv.status_code == 400


@patch("Controller.user_controller.user_service")
def test_signup_success(mock_svc, app):
    mock_svc.create_user.return_value = {"success": True, "message": "ok"}
    with app.test_client() as client:
        rv = client.post("/signup", data={
            "name": "Alice", "email": "alice@gmail.com",
            "password": "ValidPass1@", "confirm_password": "ValidPass1@"
        })
        assert rv.status_code == 201
        data = rv.get_json()
        assert data.get("success") is True


def test_login_missing_fields(app):
    with app.test_client() as client:
        rv = client.post("/login", data={})
        assert rv.status_code == 400
        assert "required" in rv.get_json().get("message", "").lower()


def test_login_invalid_email(app):
    with app.test_client() as client:
        rv = client.post("/login", data={"email": "x@yahoo.com", "password": "Pass1@word"})
        assert rv.status_code == 400
        assert "gmail" in rv.get_json().get("message", "").lower()


@patch("Controller.user_controller.user_service")
def test_login_user_not_found(mock_svc, app):
    mock_svc.login_user.return_value = {"success": False, "message": "User not found"}
    with app.test_client() as client:
        rv = client.post("/login", data={"email": "new@gmail.com", "password": "Pass1@word"})
        assert rv.status_code == 401


@patch("Controller.user_controller.user_service")
def test_login_success(mock_svc, app):
    mock_svc.login_user.return_value = {
        "success": True, "user": {"name": "U", "email": "u@gmail.com", "provider": "local"}
    }
    with app.test_client() as client:
        rv = client.post("/login", data={"email": "u@gmail.com", "password": "Pass1@word"})
        assert rv.status_code == 200
        assert rv.get_json().get("success") is True


def test_get_profile_unauthorized(app):
    with app.test_client() as client:
        rv = client.get("/profile")
        assert rv.status_code == 401


@patch("Controller.user_controller.user_service")
def test_get_profile_success(mock_svc, app):
    mock_svc.repo.find_user_by_email.return_value = {"name": "enc", "email": "enc", "provider": "local"}
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com", "name": "U"}
        with patch("Controller.user_controller.CryptoUtils") as MockCrypto:
            MockCrypto.encode.return_value = "enc"
            MockCrypto.decode.return_value = "U"
            rv = client.get("/profile")
        assert rv.status_code == 200
        data = rv.get_json()
        assert data.get("success") is True


def test_update_profile_unauthorized(app):
    with app.test_client() as client:
        rv = client.put("/profile", json={"name": "New"})
        assert rv.status_code == 401


def test_update_profile_name_required(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.put("/profile", json={})
        assert rv.status_code == 400
        assert "name" in rv.get_json().get("message", "").lower()


def test_update_profile_name_too_short(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user"] = {"email": "u@gmail.com"}
        rv = client.put("/profile", json={"name": "x"})
        assert rv.status_code == 400
