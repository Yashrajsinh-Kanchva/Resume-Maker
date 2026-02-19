"""Tests for utils.openai_client."""
import pytest
from unittest.mock import patch, MagicMock


@patch("utils.openai_client.client")
def test_call_openai_returns_content(mock_client):
    from utils.openai_client import call_openai
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Hello"))]
    )
    result = call_openai("Say hello")
    assert result == "Hello"
    mock_client.chat.completions.create.assert_called_once()
