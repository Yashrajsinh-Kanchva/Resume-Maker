"""Tests for repo.resume_repo."""
import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId


@patch("repo.resume_repo.db")
def test_resume_repo_create(mock_db):
    from repo.resume_repo import ResumeRepo
    mock_coll = MagicMock()
    mock_db.__getitem__.return_value = mock_coll
    repo = ResumeRepo()
    resume = {"user_email": "enc", "title": "R", "data": {}}
    repo.create(resume)
    mock_coll.insert_one.assert_called_once_with(resume)


@patch("repo.resume_repo.db")
def test_resume_repo_find_by_user(mock_db):
    from repo.resume_repo import ResumeRepo
    mock_coll = MagicMock()
    mock_coll.find.return_value = [{"_id": ObjectId(), "title": "R1"}]
    mock_db.__getitem__.return_value = mock_coll
    repo = ResumeRepo()
    result = repo.find_by_user("enc")
    assert len(result) == 1
    mock_coll.find.assert_called_once()


@patch("repo.resume_repo.db")
def test_resume_repo_find_by_id_invalid_returns_none(mock_db):
    from repo.resume_repo import ResumeRepo
    mock_coll = MagicMock()
    mock_coll.find_one.side_effect = Exception("InvalidId")
    mock_db.__getitem__.return_value = mock_coll
    repo = ResumeRepo()
    result = repo.find_by_id("invalid")
    assert result is None


@patch("repo.resume_repo.db")
def test_resume_repo_find_one(mock_db):
    from repo.resume_repo import ResumeRepo
    mock_coll = MagicMock()
    oid = ObjectId()
    mock_coll.find_one.return_value = {"_id": oid}
    mock_db.__getitem__.return_value = mock_coll
    repo = ResumeRepo()
    result = repo.find_one("enc", oid)
    assert result == {"_id": oid}
