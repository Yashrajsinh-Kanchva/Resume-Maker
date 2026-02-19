"""Tests for services.user_service."""
import pytest
from unittest.mock import patch, MagicMock
from DTO.user_signup_dto import UserSignupDTO
from DTO.user_login_dto import UserLoginDTO


@patch("services.user_service.UserRepo")
def test_create_user_already_exists(MockRepo):
    from services.user_service import UserService
    mock_repo = MagicMock()
    mock_repo.find_user_by_email.return_value = {"email": "enc"}
    MockRepo.return_value = mock_repo
    svc = UserService()
    dto = UserSignupDTO("A", "a@gmail.com", "Pass1@word")
    result = svc.create_user(dto)
    assert result["success"] is False
    assert "already" in result["message"].lower() or "registered" in result["message"].lower()


@patch("services.user_service.UserRepo")
def test_create_user_blocked_cannot_register(MockRepo):
    from services.user_service import UserService
    mock_repo = MagicMock()
    mock_repo.find_user_by_email.return_value = {"email": "enc", "status": "blocked"}
    MockRepo.return_value = mock_repo
    svc = UserService()
    dto = UserSignupDTO("A", "a@gmail.com", "Pass1@word")
    result = svc.create_user(dto)
    assert result["success"] is False
    assert "blocked" in result["message"].lower()


@patch("services.user_service.UserRepo")
def test_create_user_success(MockRepo):
    from services.user_service import UserService
    mock_repo = MagicMock()
    mock_repo.find_user_by_email.return_value = None
    MockRepo.return_value = mock_repo
    svc = UserService()
    dto = UserSignupDTO("Alice", "alice@gmail.com", "Pass1@word")
    result = svc.create_user(dto)
    assert result["success"] is True
    mock_repo.create_user.assert_called_once()


@patch("services.user_service.UserRepo")
def test_login_user_not_found(MockRepo):
    from services.user_service import UserService
    mock_repo = MagicMock()
    mock_repo.find_user_by_email.return_value = None
    MockRepo.return_value = mock_repo
    svc = UserService()
    dto = UserLoginDTO("x@gmail.com", "pass")
    result = svc.login_user(dto)
    assert result["success"] is False
    assert "not found" in result["message"].lower() or "user" in result["message"].lower()


@patch("services.user_service.UserRepo")
def test_login_user_blocked(MockRepo):
    from services.user_service import UserService
    mock_repo = MagicMock()
    mock_repo.find_user_by_email.return_value = {"password": "hash", "status": "blocked", "name": "Q", "email": "Q"}
    MockRepo.return_value = mock_repo
    with patch("services.user_service.check_password_hash", return_value=True):
        svc = UserService()
        dto = UserLoginDTO("x@gmail.com", "pass")
        result = svc.login_user(dto)
    assert result["success"] is False
    assert "blocked" in result["message"].lower()
