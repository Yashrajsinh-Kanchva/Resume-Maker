"""Tests for utils.validators."""
import pytest
from utils.validators import is_valid_gmail, validate_password


class TestIsValidGmail:
    def test_valid_gmail(self):
        assert is_valid_gmail("user@gmail.com") is True
        assert is_valid_gmail("a.b@gmail.com") is True

    def test_invalid_empty_or_none(self):
        assert is_valid_gmail("") is False
        assert is_valid_gmail(None) is False

    def test_invalid_contains_space(self):
        assert is_valid_gmail("user @gmail.com") is False

    def test_invalid_not_gmail(self):
        assert is_valid_gmail("user@yahoo.com") is False
        assert is_valid_gmail("user@gmail.com ") is False


class TestValidatePassword:
    def test_empty_password(self):
        ok, msg = validate_password("")
        assert ok is False
        assert "required" in msg.lower()

    def test_none_password(self):
        ok, msg = validate_password(None)
        assert ok is False

    def test_contains_space(self):
        ok, msg = validate_password("Pass1@word ")
        assert ok is False
        assert "space" in msg.lower()

    def test_too_short(self):
        ok, msg = validate_password("Ab1@")
        assert ok is False
        assert "8" in msg

    def test_no_uppercase(self):
        ok, msg = validate_password("password1@")
        assert ok is False
        assert "uppercase" in msg.lower()

    def test_no_lowercase(self):
        ok, msg = validate_password("PASSWORD1@")
        assert ok is False
        assert "lowercase" in msg.lower()

    def test_no_digit(self):
        ok, msg = validate_password("Password@")
        assert ok is False
        assert "digit" in msg.lower()

    def test_no_special(self):
        ok, msg = validate_password("Password1")
        assert ok is False
        assert "special" in msg.lower()

    def test_invalid_special_char(self):
        ok, msg = validate_password("Password1!")
        assert ok is False
        assert "Only" in msg or "$ @ #" in msg

    def test_valid_password(self):
        ok, msg = validate_password("ValidPass1@")
        assert ok is True
        assert msg == ""

    def test_valid_with_all_special_options(self):
        ok, _ = validate_password("Abcd1234$")
        assert ok is True
        ok, _ = validate_password("Abcd1234@")
        assert ok is True
        ok, _ = validate_password("Abcd1234#")
        assert ok is True
