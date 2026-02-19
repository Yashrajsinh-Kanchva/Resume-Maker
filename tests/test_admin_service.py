"""Tests for services.admin_service."""
import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId


@patch("services.admin_service.UserRepo")
def test_get_all_users(mock_repo):
    mock_repo.return_value.find_all_users.return_value = [
        {"_id": ObjectId(), "email": "enc", "name": "enc", "provider": "local", "status": "active", "role": "user"}
    ]
    from services.admin_service import AdminService
    with patch("services.admin_service.CryptoUtils") as MockCrypto:
        MockCrypto.decode.side_effect = lambda x: x if x == "enc" else "dec"
        svc = AdminService()
        result = svc.get_all_users()
    assert len(result) == 1
    assert result[0]["provider"] == "local"
    assert "email" in result[0]


@patch("services.admin_service.UserRepo")
def test_block_user(mock_repo):
    from services.admin_service import AdminService
    with patch("services.admin_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminService()
        svc.block_user("u@gmail.com")
    svc.repo.update_user.assert_called_once()
    (query, update) = svc.repo.update_user.call_args[0]
    assert update["$set"]["status"] == "blocked"
    assert {"$in": ["u@gmail.com", "enc"]} in query.values()


@patch("services.admin_service.UserRepo")
def test_login_admin_not_found(mock_repo):
    mock_repo.return_value.find_user_by_email.return_value = None
    from services.admin_service import AdminService
    with patch("services.admin_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminService()
        result = svc.login_admin("admin@gmail.com", "pass")
    assert result["success"] is False
    assert "not found" in result.get("message", "").lower()
    svc.repo.find_user_by_email.assert_called_with("enc")


@patch("services.admin_service.UserRepo")
def test_login_admin_not_admin_role(mock_repo):
    mock_repo.return_value.find_user_by_email.return_value = {"role": "user", "password": "hash"}
    from services.admin_service import AdminService
    with patch("services.admin_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminService()
        result = svc.login_admin("user@gmail.com", "pass")
    assert result["success"] is False
    assert "denied" in result.get("message", "").lower()


@patch("services.admin_service.UserRepo")
def test_login_admin_success(mock_repo):
    mock_repo.return_value.find_user_by_email.return_value = {
        "role": "admin", "password": "hash", "name": "enc", "email": "enc"
    }
    from services.admin_service import AdminService
    with patch("services.admin_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        MockCrypto.decode.return_value = "Admin"
        with patch("services.admin_service.check_password_hash", return_value=True):
            svc = AdminService()
            result = svc.login_admin("admin@gmail.com", "pass")
    assert result["success"] is True
    assert result["admin"]["role"] == "admin"


@patch("services.admin_service.UserRepo")
def test_is_admin_true(mock_repo):
    mock_repo.return_value.find_user_by_email.return_value = {"role": "admin"}
    from services.admin_service import AdminService
    with patch("services.admin_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminService()
        assert svc.is_admin("admin@gmail.com") is True


@patch("services.admin_service.UserRepo")
def test_is_admin_false(mock_repo):
    mock_repo.return_value.find_user_by_email.return_value = {"role": "user"}
    from services.admin_service import AdminService
    with patch("services.admin_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminService()
        assert svc.is_admin("user@gmail.com") is False


def test_is_admin_empty_email_returns_false():
    from services.admin_service import AdminService
    with patch("services.admin_service.UserRepo"):
        with patch("services.admin_service.CryptoUtils"):
            svc = AdminService()
            assert svc.is_admin("") is False
            assert svc.is_admin("   ") is False


@patch("services.admin_service.UserRepo")
def test_unblock_user(mock_repo):
    from services.admin_service import AdminService
    with patch("services.admin_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminService()
        svc.unblock_user("u@gmail.com")
    (query, update) = svc.repo.update_user.call_args[0]
    assert update["$set"]["status"] == "active"


@patch("services.admin_service.UserRepo")
def test_delete_user(mock_repo):
    from services.admin_service import AdminService
    with patch("services.admin_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminService()
        svc.delete_user("u@gmail.com")
    svc.repo.delete_user.assert_called_once()
    (query,) = svc.repo.delete_user.call_args[0]
    assert {"$in": ["u@gmail.com", "enc"]} in query.values()
