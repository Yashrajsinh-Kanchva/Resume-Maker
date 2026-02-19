"""Tests for DTO.user_signup_dto."""
import pytest
from DTO.user_signup_dto import UserSignupDTO


class TestUserSignupDTO:
    def test_is_valid_with_all_fields(self):
        dto = UserSignupDTO("Alice", "alice@gmail.com", "Pass1@word")
        assert dto.is_valid() is True

    def test_strips_name_and_lowercases_email(self):
        dto = UserSignupDTO("  Bob  ", "  Bob@Gmail.COM  ", "pass")
        assert dto.name == "Bob"
        assert dto.email == "bob@gmail.com"

    def test_invalid_missing_name(self):
        dto = UserSignupDTO("", "a@gmail.com", "pass")
        assert dto.is_valid() is False

    def test_invalid_missing_email(self):
        dto = UserSignupDTO("A", "", "pass")
        assert dto.is_valid() is False

    def test_invalid_missing_password(self):
        dto = UserSignupDTO("A", "a@gmail.com", "")
        assert dto.is_valid() is False

    def test_to_dict(self):
        dto = UserSignupDTO("C", "c@gmail.com", "pwd")
        assert dto.to_dict() == {"name": "C", "email": "c@gmail.com", "password": "pwd"}
