"""Tests for utils.intent_mapper."""
import pytest
from utils.intent_mapper import is_website_question, detect_intent


class TestIsWebsiteQuestion:
    def test_contains_resume(self):
        assert is_website_question("I want a resume") is True
        assert is_website_question("RESUME") is True

    def test_contains_other_keywords(self):
        assert is_website_question("how to build a cv") is True
        assert is_website_question("pricing") is True
        assert is_website_question("contact support") is True

    def test_unrelated_text(self):
        assert is_website_question("what is the weather") is False
        assert is_website_question("hello") is False


class TestDetectIntent:
    def test_contact_intent(self):
        assert detect_intent("contact us") == "GO_TO_CONTACT"
        assert detect_intent("I need support") == "GO_TO_CONTACT"

    def test_pricing_intent(self):
        assert detect_intent("what is the price") == "GO_TO_PRICING"
        assert detect_intent("pricing") == "GO_TO_PRICING"

    def test_feedback_intent(self):
        assert detect_intent("give feedback") == "GO_TO_FEEDBACK"
        assert detect_intent("rate this") == "GO_TO_FEEDBACK"
        assert detect_intent("review") == "GO_TO_FEEDBACK"

    def test_faq_intent(self):
        assert detect_intent("faq") == "SCROLL_FAQ"

    def test_none_intent(self):
        assert detect_intent("hello world") == "NONE"
        assert detect_intent("random text") == "NONE"
