"""Tests for utils.rate_limiter."""
import pytest
from unittest.mock import patch, MagicMock


@patch("utils.rate_limiter.redis_client")
def test_is_rate_limited_under_limit(mock_redis):
    mock_redis.incr.return_value = 5
    from utils.rate_limiter import is_rate_limited
    assert is_rate_limited("client1") is False
    mock_redis.incr.assert_called_once_with("rate:client1")


@patch("utils.rate_limiter.redis_client")
def test_is_rate_limited_over_limit(mock_redis):
    mock_redis.incr.return_value = 25
    from utils.rate_limiter import is_rate_limited
    assert is_rate_limited("client2") is True


@patch("utils.rate_limiter.redis_client")
def test_is_rate_limited_redis_error_allows_request(mock_redis):
    mock_redis.incr.side_effect = Exception("Redis down")
    from utils.rate_limiter import is_rate_limited
    assert is_rate_limited("client3") is False
