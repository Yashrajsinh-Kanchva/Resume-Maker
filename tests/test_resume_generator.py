"""Tests for ai.resume_generator."""
import pytest
from unittest.mock import patch, MagicMock


def test_suggest_from_role_empty_returns_empty_dict():
    from ai.resume_generator import suggest_from_role
    result = suggest_from_role("")
    assert result == {"title": "", "summary": "", "skills": [], "job_description": ""}
    result = suggest_from_role("   ")
    assert result == {"title": "", "summary": "", "skills": [], "job_description": ""}


@patch("ai.resume_generator.client")
def test_suggest_from_role_with_response(mock_client):
    from ai.resume_generator import suggest_from_role
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"title": "Dev", "summary": "S", "skills": ["Python"], "job_description": "JD"}'))]
    )
    result = suggest_from_role("Developer")
    assert result["title"] == "Dev"
    assert result["skills"] == ["Python"]


@patch("ai.resume_generator.client")
def test_generate_ai_resume(mock_client):
    from ai.resume_generator import generate_ai_resume
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"summary": "Hi", "education": {}, "experience": [], "skills": []}'))]
    )
    result = generate_ai_resume({"name": "Jane"})
    assert "summary" in result
    assert result["summary"] == "Hi"
