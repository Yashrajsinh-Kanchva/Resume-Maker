"""Tests for services.admin_data_service."""
import pytest
from unittest.mock import patch, MagicMock


@patch("services.admin_data_service.db")
def test_dashboard(mock_db):
    mock_users = MagicMock()
    mock_users.count_documents.return_value = 5
    mock_users.find.return_value = [
        {"provider": "local"}, {"provider": "google"}, {"provider": "local"}
    ]
    mock_resumes = MagicMock()
    mock_resumes.count_documents.return_value = 5
    mock_feedbacks = MagicMock()
    mock_feedbacks.count_documents.return_value = 5
    mock_db.__getitem__.side_effect = lambda k: (
        mock_users if k == "users" else mock_resumes if k == "resumes" else mock_feedbacks
    )
    from services.admin_data_service import AdminDataService
    svc = AdminDataService()
    result = svc.dashboard()
    assert result["total_users"] == 5
    assert result["total_resumes"] == 5
    assert result["total_feedbacks"] == 5
    assert "providers" in result
    assert result["providers"]["local"] == 2
    assert result["providers"]["google"] == 1


@patch("services.admin_data_service.db")
def test_users(mock_db):
    mock_users = MagicMock()
    mock_users.find.return_value = [
        {"name": "enc", "email": "enc", "provider": "local", "role": "user", "status": "active", "created_at": None}
    ]
    mock_db.__getitem__.return_value = mock_users
    from services.admin_data_service import AdminDataService
    with patch("services.admin_data_service.CryptoUtils") as MockCrypto:
        MockCrypto.decode.return_value = "Decoded"
        svc = AdminDataService()
        result = svc.users()
    assert len(result) == 1
    assert result[0]["name"] == "Decoded"
    assert result[0]["provider"] == "local"


@patch("services.admin_data_service.db")
def test_resumes(mock_db):
    mock_resumes = MagicMock()
    mock_resumes.count_documents.return_value = 10
    mock_resumes.aggregate.return_value = [{"_id": "enc1", "count": 3}]
    mock_db.__getitem__.return_value = mock_resumes
    from services.admin_data_service import AdminDataService
    svc = AdminDataService()
    result = svc.resumes()
    assert result["total"] == 10
    assert "per_user" in result
    assert len(result["per_user"]) == 1


def test_health():
    from services.admin_data_service import AdminDataService
    svc = AdminDataService()
    result = svc.health()
    assert result["flask"] == "ok"
    assert result["mongo"] == "connected"
    assert result["redis"] == "connected"
