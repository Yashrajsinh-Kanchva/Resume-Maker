"""Tests for services.skill_frequency_service (in addition to existing test_skill_suggestion_service)."""
import pytest
from unittest.mock import patch


@patch("services.skill_frequency_service.resume_service")
def test_get_skill_frequency_empty_resumes(mock_svc):
    from services.skill_frequency_service import get_skill_frequency
    mock_svc.get_user_resumes.return_value = []
    result = get_skill_frequency("u@gmail.com")
    assert result == {}


@patch("services.skill_frequency_service.resume_service")
def test_get_skill_frequency_aggregates_skills(mock_svc):
    from services.skill_frequency_service import get_skill_frequency
    mock_svc.get_user_resumes.return_value = [{"_id": "id1"}]
    mock_svc.get_resume_by_id.return_value = {"data": {"step4": ["Python", "Java", "Python"]}}
    result = get_skill_frequency("u@gmail.com")
    assert "python" in result
    assert result["python"] == 2
    assert "java" in result
