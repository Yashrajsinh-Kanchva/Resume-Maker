"""Tests for services.skill_suggestion_service."""
import pytest
from services.skill_suggestion_service import suggest_skills


class TestSkillSuggestionService:
    def test_suggest_python(self):
        result = suggest_skills("py")
        assert "Python" in result or "python" in result

    def test_suggest_java(self):
        result = suggest_skills("jav")
        assert "Java" in result
        assert "Javascript" in result

    def test_suggest_case_insensitive(self):
        result = suggest_skills("PY")
        assert "Python" in result

    def test_no_match(self):
        result = suggest_skills("xyz")
        assert result == []

    def test_empty_prefix(self):
        result = suggest_skills("")
        assert isinstance(result, list)
        assert len(result) > 0
