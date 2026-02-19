"""Tests for services.ai_resume_service."""
import pytest
from unittest.mock import patch, MagicMock
from services.ai_resume_service import (
    _to_list,
    _merge_skills,
    _normalize_skills_from_payload,
    _build_step1,
    _build_step2,
    _build_resume_data,
)


class TestToList:
    def test_empty(self):
        assert _to_list(None) == []
        assert _to_list("") == []

    def test_list(self):
        assert _to_list(["a", "b"]) == ["a", "b"]

    def test_string_splits_by_newline(self):
        assert _to_list("a\nb\nc") == ["a", "b", "c"]


class TestMergeSkills:
    def test_user_skills_first(self):
        result = _merge_skills(["Python", "Java"], [])
        assert result == ["Python", "Java"]

    def test_ai_skills_appended_unique(self):
        result = _merge_skills(["Python"], [{"name": "Java"}, "SQL"])
        assert "Python" in result
        assert "Java" in result
        assert "SQL" in result

    def test_dedupe(self):
        result = _merge_skills(["Python"], ["Python", "Java"])
        assert result.count("Python") == 1


class TestNormalizeSkillsFromPayload:
    def test_list(self):
        assert _normalize_skills_from_payload({"skills": ["a", "b"]}) == ["a", "b"]

    def test_string_splits_newline(self):
        result = _normalize_skills_from_payload({"skills": "a\nb"})
        assert result == ["a", "b"]

    def test_empty(self):
        assert _normalize_skills_from_payload({}) == []


class TestBuildStep1:
    def test_basic(self):
        step1 = _build_step1({"name": "Jane", "title": "Dev"}, {"summary": "AI summary"})
        assert step1["name"] == "Jane"
        assert step1["title"] == "Dev"
        assert step1["summary"] == "AI summary"


class TestBuildStep2:
    def test_basic(self):
        step2 = _build_step2({"institution": "MIT", "degree": "BS"})
        assert step2["institution"] == "MIT"
        assert step2["degree"] == "BS"


class TestBuildResumeData:
    def test_structure(self):
        data = _build_resume_data(
            {"name": "A"},
            {"degree": "BS"},
            [{"jobTitle": "Dev"}],
            {"summary": "S", "skills": []},
            ["Python"]
        )
        assert "step1" in data
        assert "step2" in data
        assert data["step3"] == [{"jobTitle": "Dev"}]
        assert "Python" in data["step4"]


@patch("services.ai_resume_service.generate_ai_resume")
@patch("services.ai_resume_service.resume_repo")
def test_create_ai_resume(mock_repo, mock_gen):
    from services.ai_resume_service import create_ai_resume
    mock_gen.return_value = {"summary": "S", "skills": ["Python"], "education": {}, "experience": []}
    mock_repo.create.return_value = MagicMock(inserted_id="507f1f77bcf86cd799439011")
    result = create_ai_resume("u@gmail.com", {
        "role": "Developer",
        "personal": {"name": "Jane"},
        "education": {},
        "experience": [],
        "template": "professionalBlue"
    })
    assert result == "507f1f77bcf86cd799439011"
    mock_repo.create.assert_called_once()
