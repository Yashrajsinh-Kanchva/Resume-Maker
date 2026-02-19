"""Tests for repo.user_repo."""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone


@patch("repo.user_repo.db")
def test_user_repo_find_by_email(mock_db):
    from repo.user_repo import UserRepo
    mock_coll = MagicMock()
    mock_coll.find_one.return_value = {"email": "enc", "name": "U"}
    mock_db.__getitem__.return_value = mock_coll
    repo = UserRepo()
    result = repo.find_user_by_email("enc@x.com")
    assert result == {"email": "enc", "name": "U"}
    mock_coll.find_one.assert_called_once_with({"email": "enc@x.com"})


@patch("repo.user_repo.db")
def test_user_repo_create_user_sets_defaults(mock_db):
    from repo.user_repo import UserRepo
    mock_coll = MagicMock()
    mock_db.__getitem__.return_value = mock_coll
    repo = UserRepo()
    data = {"email": "e", "password": "p"}
    repo.create_user(data)
    assert "created_at" in data
    assert data.get("status") == "active"
    assert data.get("role") == "user"
    mock_coll.insert_one.assert_called_once()


@patch("repo.user_repo.db")
def test_user_repo_find_all_users(mock_db):
    from repo.user_repo import UserRepo
    mock_coll = MagicMock()
    mock_coll.find.return_value = [{"email": "a"}]
    mock_db.__getitem__.return_value = mock_coll
    repo = UserRepo()
    result = repo.find_all_users()
    assert len(result) == 1
    assert result[0]["email"] == "a"
