"""Tests for services.chat_service."""
import pytest
from unittest.mock import patch, MagicMock


def test_process_chat_empty_message():
    from services.chat_service import process_chat
    reply, intent = process_chat("")
    assert "empty" in reply.lower() or "cannot" in reply.lower()
    assert intent == "NONE"
    reply, intent = process_chat("   ")
    assert intent == "NONE"


def test_process_chat_off_topic_returns_gate_message():
    from services.chat_service import process_chat
    reply, intent = process_chat("What is the weather today?")
    assert "only help" in reply.lower() or "resume maker" in reply.lower()
    assert intent == "NONE"


@patch("services.chat_service.redis_client")
@patch("services.chat_service.requests.post")
def test_process_chat_website_question_calls_openai(mock_post, mock_redis):
    from services.chat_service import process_chat
    mock_redis.get.return_value = None
    mock_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "Go to Documents and click Download."}}]
    }
    mock_post.return_value.raise_for_status = MagicMock()
    reply, intent = process_chat("How do I download my resume?")
    assert mock_post.called
    assert reply
    assert intent in ("NONE", "GO_TO_CONTACT", "SCROLL_FAQ", "GO_TO_PRICING", "GO_TO_FEEDBACK")


@patch("services.chat_service.redis_client")
def test_process_chat_cache_hit(mock_redis):
    from services.chat_service import process_chat
    mock_redis.get.return_value = "Cached reply||GO_TO_CONTACT"
    reply, intent = process_chat("how to download resume")
    assert reply == "Cached reply"
    assert intent == "GO_TO_CONTACT"
