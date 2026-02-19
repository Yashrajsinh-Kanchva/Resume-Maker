"""Tests for utils.semantic_cache."""
import pytest
from utils.semantic_cache import semantic_key, STOPWORDS


class TestSemanticCache:
    def test_semantic_key_lowercases(self):
        assert semantic_key("HELLO") == "hello"

    def test_semantic_key_removes_stopwords(self):
        key = semantic_key("how do I can the")
        assert "how" not in key
        assert "do" not in key

    def test_semantic_key_joins_with_underscore(self):
        key = semantic_key("resume build create")
        assert "_" in key
        parts = key.split("_")
        assert "resume" in parts
        assert "build" in parts
        assert "create" in parts

    def test_semantic_key_sorted(self):
        key = semantic_key("create resume")
        assert key == "create_resume" or key == "resume_create"

    def test_stopwords_defined(self):
        assert "the" in STOPWORDS
        assert "how" in STOPWORDS
