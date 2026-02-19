"""Tests for services.admin_user_action_service."""
import pytest
from unittest.mock import patch, MagicMock


@patch("services.admin_user_action_service.db")
def test_block_user(mock_db):
    mock_coll = MagicMock()
    mock_coll.update_one.return_value = MagicMock(modified_count=1)
    mock_db.__getitem__.return_value = mock_coll
    from services.admin_user_action_service import AdminUserActionService
    with patch("services.admin_user_action_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminUserActionService()
        result = svc.block_user("u@gmail.com")
    assert result["success"] is True
    mock_coll.update_one.assert_called_once()
    assert mock_coll.update_one.call_args[0][1]["$set"]["status"] == "blocked"


@patch("services.admin_user_action_service.db")
def test_unblock_user(mock_db):
    mock_coll = MagicMock()
    mock_coll.update_one.return_value = MagicMock(modified_count=1)
    mock_db.__getitem__.return_value = mock_coll
    from services.admin_user_action_service import AdminUserActionService
    with patch("services.admin_user_action_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminUserActionService()
        result = svc.unblock_user("u@gmail.com")
    assert result["success"] is True
    assert mock_coll.update_one.call_args[0][1]["$set"]["status"] == "active"


@patch("services.admin_user_action_service.db")
def test_delete_user_cannot_delete_admin(mock_db):
    mock_users = MagicMock()
    mock_users.find_one.return_value = {"email": "enc", "role": "admin"}
    mock_db.__getitem__.side_effect = lambda k: mock_users if k == "users" else MagicMock()
    from services.admin_user_action_service import AdminUserActionService
    with patch("services.admin_user_action_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminUserActionService()
        result = svc.delete_user("admin@gmail.com")
    assert result["success"] is False
    assert "admin" in result.get("message", "").lower()
    mock_users.delete_one.assert_not_called()


@patch("services.admin_user_action_service.db")
def test_delete_user_success(mock_db):
    mock_users = MagicMock()
    mock_users.find_one.return_value = {"email": "enc", "role": "user"}
    mock_resumes = MagicMock()
    mock_db.__getitem__.side_effect = lambda k: mock_users if k == "users" else mock_resumes
    from services.admin_user_action_service import AdminUserActionService
    with patch("services.admin_user_action_service.CryptoUtils") as MockCrypto:
        MockCrypto.encode.return_value = "enc"
        svc = AdminUserActionService()
        result = svc.delete_user("user@gmail.com")
    assert result["success"] is True
    mock_users.delete_one.assert_called_once_with({"email": "enc"})
    mock_resumes.delete_many.assert_called_once_with({"user_email": "enc"})
