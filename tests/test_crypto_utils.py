"""Tests for utils.crypto_utils."""
import pytest
from utils.crypto_utils import CryptoUtils


class TestCryptoUtils:
    def test_encode_decode_roundtrip(self):
        text = "secret message"
        encoded = CryptoUtils.encode(text)
        assert encoded != text
        decoded = CryptoUtils.decode(encoded)
        assert decoded == text

    def test_safe_decode_valid(self):
        text = "hello"
        encoded = CryptoUtils.encode(text)
        assert CryptoUtils.safe_decode(encoded) == text

    def test_safe_decode_invalid_returns_original(self):
        result = CryptoUtils.safe_decode("not-valid-base64!!!")
        assert result == "not-valid-base64!!!"

    def test_encode_produces_base64(self):
        import base64
        encoded = CryptoUtils.encode("x")
        try:
            base64.b64decode(encoded.encode("utf-8"))
        except Exception:
            pytest.fail("Should be valid base64")
