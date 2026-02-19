"""Tests for Controller.reset_password_controller."""
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    from Controller.page_controller import page_bp
    from Controller.reset_password_controller import reset_password_bp
    app.register_blueprint(page_bp)
    app.register_blueprint(reset_password_bp)
    return app


def test_reset_password_get_invalid_token(app):
    with app.test_client() as client:
        rv = client.get("/api/reset-password/invalid-token-here")
        assert rv.status_code == 400
        data = rv.get_json()
        assert data.get("success") is False
        assert "invalid" in data.get("message", "").lower() or "expired" in data.get("message", "").lower()


def test_reset_password_post_invalid_token(app):
    with app.test_client() as client:
        rv = client.post("/api/reset-password/invalid-token", data={"password": "NewPass1@"})
        assert rv.status_code == 400


def test_reset_password_post_missing_password(app):
    from itsdangerous import URLSafeTimedSerializer
    serializer = URLSafeTimedSerializer("test-secret")
    token = serializer.dumps("user@gmail.com", salt="password-reset")
    with app.test_client() as client:
        rv = client.post(f"/api/reset-password/{token}", data={})
        assert rv.status_code == 400
        assert "password" in rv.get_json().get("message", "").lower()


@patch("Controller.reset_password_controller.get_users_collection")
@patch("utils.crypto_utils.CryptoUtils")
def test_reset_password_post_success(MockCrypto, mock_get_coll, app):
    from itsdangerous import URLSafeTimedSerializer
    MockCrypto.encode.return_value = "enc"
    serializer = URLSafeTimedSerializer("test-secret")
    token = serializer.dumps("user@gmail.com", salt="password-reset")
    mock_coll = MagicMock()
    mock_get_coll.return_value = mock_coll
    with app.test_client() as client:
        rv = client.post(f"/api/reset-password/{token}", data={"password": "NewValid1@"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data.get("success") is True
    mock_coll.update_one.assert_called_once()
