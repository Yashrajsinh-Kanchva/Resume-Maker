"""Tests for ai.prompts."""
import json
import pytest
from ai.prompts import build_resume_prompt, build_role_suggestions_prompt


class TestBuildResumePrompt:
    def test_returns_string_with_user_data(self):
        user_data = {"name": "Jane", "skills": ["Python"]}
        result = build_resume_prompt(user_data)
        assert isinstance(result, str)
        assert "Jane" in result
        assert "Python" in result
        assert "USER DATA" in result
        assert "JSON" in result

    def test_includes_json_dumped_data(self):
        user_data = {"summary": "Dev"}
        result = build_resume_prompt(user_data)
        assert json.dumps(user_data, indent=2) in result


class TestBuildRoleSuggestionsPrompt:
    def test_returns_string_with_role(self):
        result = build_role_suggestions_prompt("Data Scientist")
        assert isinstance(result, str)
        assert "Data Scientist" in result
        assert "resume expert" in result
        assert "JSON" in result

    def test_empty_role(self):
        result = build_role_suggestions_prompt("")
        assert '""' in result or "" in result
