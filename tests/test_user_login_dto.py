"""Tests for DTO.user_login_dto."""
import pytest
from DTO.user_login_dto import UserLoginDTO


class TestUserLoginDTO:
    def test_is_valid_with_email_and_password(self):
        dto = UserLoginDTO("user@gmail.com", "pass123")
        assert dto.is_valid() is True

    def test_is_valid_strips_and_lowercases_email(self):
        dto = UserLoginDTO("  User@Gmail.COM  ", "pass")
        assert dto.email == "user@gmail.com"
        assert dto.is_valid() is True

    def test_invalid_missing_email(self):
        dto = UserLoginDTO("", "pass")
        assert dto.is_valid() is False
        dto = UserLoginDTO(None, "pass")
        assert dto.is_valid() is False

    def test_invalid_missing_password(self):
        dto = UserLoginDTO("a@gmail.com", None)
        assert dto.is_valid() is False

    def test_to_dict(self):
        dto = UserLoginDTO("u@gmail.com", "secret")
        assert dto.to_dict() == {"email": "u@gmail.com", "password": "secret"}
