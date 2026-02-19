"""Tests for config.openai_config."""
import pytest
from config import openai_config


def test_openai_model_defined():
    assert hasattr(openai_config, "OPENAI_MODEL")
    assert openai_config.OPENAI_MODEL


def test_openai_headers_contain_auth_and_content_type():
    assert "Authorization" in openai_config.OPENAI_HEADERS
    assert "Content-Type" in openai_config.OPENAI_HEADERS
    assert openai_config.OPENAI_HEADERS.get("Content-Type") == "application/json"


def test_openai_url():
    assert "openai.com" in openai_config.OPENAI_URL
