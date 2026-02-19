"""Tests for services.resume_service."""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from bson import ObjectId


@patch("services.resume_service.ResumeRepo")
def test_create_resume_invalid_payload(MockRepo):
    from services.resume_service import ResumeService
    svc = ResumeService()
    assert svc.create_resume("u@x.com", {}) == {"success": False, "message": "Invalid resume data"}
    assert svc.create_resume("u@x.com", None) == {"success": False, "message": "Invalid resume data"}


@patch("services.resume_service.ResumeRepo")
def test_create_resume_success(MockRepo):
    from services.resume_service import ResumeService
    mock_repo = MagicMock()
    MockRepo.return_value = mock_repo
    svc = ResumeService()
    result = svc.create_resume("u@gmail.com", {"data": {"step1": {}}, "title": "My Resume"})
    assert result["success"] is True
    mock_repo.create.assert_called_once()


@patch("services.resume_service.ResumeRepo")
def test_get_user_resumes(MockRepo):
    from services.resume_service import ResumeService
    mock_repo = MagicMock()
    mock_repo.find_by_user.return_value = [{"_id": ObjectId(), "title": "R1"}]
    MockRepo.return_value = mock_repo
    svc = ResumeService()
    result = svc.get_user_resumes("u@gmail.com")
    assert len(result) == 1
    assert result[0]["title"] == "R1"
    assert isinstance(result[0]["_id"], str)


@patch("services.resume_service.ResumeRepo")
def test_get_resume_by_id_invalid_returns_none(MockRepo):
    from services.resume_service import ResumeService
    mock_repo = MagicMock()
    MockRepo.return_value = mock_repo
    svc = ResumeService()
    assert svc.get_resume_by_id("") is None
    assert svc.get_resume_by_id(None) is None
    assert svc.get_resume_by_id(123) is None


@patch("services.resume_service.ResumeRepo")
def test_get_resume_by_id_found(MockRepo):
    from services.resume_service import ResumeService
    oid = ObjectId()
    mock_repo = MagicMock()
    mock_repo.find_by_id.return_value = {"_id": oid, "title": "R1"}
    MockRepo.return_value = mock_repo
    svc = ResumeService()
    result = svc.get_resume_by_id(str(oid))
    assert result is not None
    assert result["title"] == "R1"
