"""Tests for services.admin_analytics_service."""
import pytest
from unittest.mock import patch, MagicMock


@patch("services.admin_analytics_service.db")
def test_get_analytics(mock_db):
    mock_coll = MagicMock()
    mock_coll.aggregate.return_value = []
    mock_db.__getitem__.return_value = mock_coll
    from services.admin_analytics_service import AdminAnalyticsService
    svc = AdminAnalyticsService()
    result = svc.get_analytics()
    assert "users_over_time" in result
    assert "resumes_over_time" in result
    assert "top_users" in result
    assert isinstance(result["users_over_time"], list)
    assert isinstance(result["top_users"], list)
