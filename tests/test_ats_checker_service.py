"""Tests for services.ats_checker_service."""
import pytest
from services.ats_checker_service import (
    _pick_final_similarity,
    _fallback_ats_suggestions,
    _step1_parts,
    _step4_skills_parts,
    _step2_education_parts,
    _single_experience_parts,
    _step3_experience_parts,
    ATSCheckerService,
)


class TestPickFinalSimilarity:
    def test_uses_overlap_when_tfidf_low(self):
        assert _pick_final_similarity(3.0, 20.0) == min(20.0 * 1.2, 80.0)

    def test_uses_overlap_when_tfidf_very_low(self):
        # tfidf < 5 and overlap > 5 => use overlap * 1.2 capped at 80
        result = _pick_final_similarity(0.05, 30.0)
        assert result == min(30.0 * 1.2, 80.0)

    def test_returns_max_of_tfidf_and_overlap(self):
        result = _pick_final_similarity(50.0, 40.0)
        assert result == max(50.0, 40.0 * 0.9)


class TestFallbackAtsSuggestions:
    def test_missing_keywords_added(self):
        s = _fallback_ats_suggestions(["python", "java"], [], "Review resume")
        assert any("python" in x.lower() for x in s)

    def test_table_issue_suggestion(self):
        s = _fallback_ats_suggestions([], ["Tables detected"], "Review", include_formatting_detail=True)
        assert any("table" in x.lower() for x in s)

    def test_empty_returns_default(self):
        s = _fallback_ats_suggestions([], [], "Default message")
        assert s == ["Default message"]


class TestStepParts:
    def test_step1_parts(self):
        step1 = {"name": "Jane", "title": "Dev", "summary": "Summary"}
        assert _step1_parts(step1) == ["Jane", "Dev", "Summary"]
        assert _step1_parts({}) == []

    def test_step4_skills_parts(self):
        assert "Python" in " ".join(_step4_skills_parts([{"name": "Python"}, "Java"]))
        assert _step4_skills_parts([]) == []

    def test_step2_education_parts(self):
        step2 = {"degree": "BS", "institution": "MIT"}
        parts = _step2_education_parts(step2)
        assert "BS" in parts and "MIT" in parts

    def test_single_experience_parts(self):
        exp = {"jobTitle": "Dev", "employer": "Co", "description": "Did stuff"}
        parts = _single_experience_parts(exp)
        assert "Dev" in parts and "Co" in parts and "Did stuff" in parts

    def test_step3_experience_parts(self):
        step3 = [{"jobTitle": "A", "employer": "B"}]
        parts = _step3_experience_parts(step3)
        assert "A" in parts and "B" in parts


class TestATSCheckerService:
    def test_detect_sections_from_data(self):
        svc = ATSCheckerService()
        data = {
            "step1": {"summary": "I am a dev"},
            "step2": {"degree": "BS"},
            "step3": [{"jobTitle": "Dev"}],
            "step4": ["Python"],
        }
        sections = svc._detect_sections_from_data(data)
        assert sections["summary"] is True
        assert sections["skills"] is True
        assert sections["experience"] is True
        assert sections["education"] is True

    def test_calculate_structure_score(self):
        svc = ATSCheckerService()
        assert svc._calculate_structure_score({"skills": True, "experience": True, "education": True}) == 30.0
        assert svc._calculate_structure_score({}) == 0.0

    def test_calculate_formatting_score(self):
        svc = ATSCheckerService()
        assert svc._calculate_formatting_score([]) == 20.0
        assert svc._calculate_formatting_score(["Tables detected"]) < 20.0

    def test_calculate_ats_score(self):
        svc = ATSCheckerService()
        score = svc._calculate_ats_score(50.0, 30.0, 20.0)
        assert 0 <= score <= 100

    def test_find_missing_keywords(self):
        svc = ATSCheckerService()
        missing = svc._find_missing_keywords(["python", "java", "the"], ["python"])
        assert "java" in missing
        assert "the" not in missing  # common word filtered

    def test_check_resume_from_data_empty_returns_error(self):
        svc = ATSCheckerService()
        result = svc.check_resume_from_data({}, "JD here")
        assert "error" in result or result.get("ats_score") == 0

    def test_check_resume_from_data_short_text_returns_error(self):
        svc = ATSCheckerService()
        result = svc.check_resume_from_data({"step1": {"name": "x"}}, "Job description with many words here")
        assert "error" in result or result.get("ats_score") == 0

    def test_check_resume_from_data_sufficient_data(self):
        svc = ATSCheckerService()
        resume_data = {
            "step1": {"name": "Jane Doe", "title": "Software Engineer", "summary": "Experienced developer with Python and Java."},
            "step2": {"degree": "BS CS", "institution": "University"},
            "step3": [{"jobTitle": "Developer", "employer": "Tech Co", "description": "Built systems with Python and APIs."}],
            "step4": ["Python", "Java", "SQL"],
        }
        result = svc.check_resume_from_data(resume_data, "We need Python and Java developers with SQL experience.")
        assert "ats_score" in result
        assert 0 <= result["ats_score"] <= 100
        assert "keyword_match_percent" in result or "error" in result
