"""Tests for services.resume_score_service."""
import pytest
from services.resume_score_service import (
    calculate_resume_score,
    _looks_like_garbage,
    _validate_resume_data,
    _profile_score,
    _summary_quality_score,
    _skills_score,
    _education_score,
)


class TestLooksLikeGarbage:
    def test_empty_or_none_returns_false(self):
        assert _looks_like_garbage("") is False
        assert _looks_like_garbage(None) is False

    def test_short_string_true(self):
        assert _looks_like_garbage("a") is True

    def test_mostly_digits_true(self):
        assert _looks_like_garbage("11111") is True
        assert _looks_like_garbage("1234567a") is True  # 7/8 digits >= 0.7

    def test_repeated_char_true(self):
        assert _looks_like_garbage("aaa") is True

    def test_valid_name_false(self):
        assert _looks_like_garbage("John Doe", "name") is False


class TestValidateResumeData:
    def test_empty_data_no_warnings(self):
        assert _validate_resume_data({}) == []

    def test_missing_name_warning(self):
        data = {"step1": {"name": ""}}
        w = _validate_resume_data(data)
        assert any("name" in x.lower() for x in w)

    def test_invalid_email_warning(self):
        data = {"step1": {"email": "bad"}}
        w = _validate_resume_data(data)
        assert any("email" in x.lower() for x in w)


class TestCalculateResumeScore:
    def test_empty_resume(self):
        score, breakdown, warnings = calculate_resume_score({})
        assert score == 0
        assert "Profile" in breakdown
        assert "Skills" in breakdown

    def test_resume_with_data(self):
        resume = {
            "data": {
                "step1": {"name": "Jane", "title": "Engineer", "summary": "A great developer with 5 years experience."},
                "step2": {"degree": "BS CS", "institution": "MIT"},
                "step3": [{"jobTitle": "Dev", "employer": "Co", "description": "Did things with Python and Java."}],
                "step4": ["Python", "Java", "SQL"],
            }
        }
        score, breakdown, _ = calculate_resume_score(resume)
        assert 0 <= score <= 100
        assert breakdown["Profile"] > 0
        assert breakdown["Skills"] > 0
        assert breakdown["Education"] > 0

    def test_profile_score(self):
        step1 = {"name": "Alice", "title": "Dev", "summary": "Summary here"}
        assert _profile_score(step1) > 0
        assert _profile_score({}) == 0.0

    def test_summary_quality_score(self):
        long_summary = (
            "This is a unique professional summary for testing the resume score module. "
            "It contains enough characters to pass the length check and is not placeholder text."
        )
        assert len(long_summary) >= 100
        assert _summary_quality_score({"summary": long_summary}) == 15.0
        assert _summary_quality_score({"summary": ""}) == 0.0

    def test_skills_score(self):
        assert _skills_score(["a", "b", "c"]) > 0
        assert _skills_score([]) == 0.0

    def test_education_score(self):
        assert _education_score({"degree": "BS", "institution": "U"}) > 0
        assert _education_score({}) == 0.0
