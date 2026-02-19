"""Tests for services.resume_ranking_service."""
import pytest
from unittest.mock import patch, MagicMock
from services.resume_ranking_service import rank_resumes


@patch("services.resume_ranking_service.resume_service")
def test_rank_resumes_empty(mock_svc):
    mock_svc.get_resume_by_id.return_value = {"data": {}}
    result = rank_resumes([])
    assert result == []


@patch("services.resume_ranking_service.resume_service")
def test_rank_resumes_returns_ranked_with_rank_field(mock_svc):
    mock_svc.get_resume_by_id.return_value = {"data": {"step1": {"name": "A"}, "step2": {}, "step3": [], "step4": []}}
    resumes = [{"_id": "id1"}, {"_id": "id2"}]
    result = rank_resumes(resumes)
    assert len(result) == 2
    assert result[0].get("rank") == 1
    assert result[1].get("rank") == 2
    assert "score" in result[0]
