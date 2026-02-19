"""Tests for DTO.chat_dto."""
import pytest
from DTO.chat_dto import ChatRequestDTO, ChatResponseDTO


class TestChatRequestDTO:
    def test_message_stored(self):
        dto = ChatRequestDTO("hello")
        assert dto.message == "hello"


class TestChatResponseDTO:
    def test_to_dict(self):
        dto = ChatResponseDTO("Hi there", "GO_TO_CONTACT")
        assert dto.to_dict() == {"reply": "Hi there", "intent": "GO_TO_CONTACT"}

    def test_reply_and_intent_stored(self):
        dto = ChatResponseDTO("ok", "NONE")
        assert dto.reply == "ok"
        assert dto.intent == "NONE"
