"""Tests for DS.trie."""
import pytest
from DS.trie import Trie


class TestTrie:
    def test_insert_and_starts_with(self):
        t = Trie()
        t.insert("hello")
        t.insert("help")
        t.insert("heap")
        assert set(t.starts_with("he")) == {"hello", "help", "heap"}
        assert "hello" in t.starts_with("hel")
        assert "help" in t.starts_with("hel")

    def test_empty_prefix_returns_all(self):
        t = Trie()
        t.insert("a")
        t.insert("ab")
        result = t.starts_with("")
        assert "a" in result
        assert "ab" in result

    def test_no_match_returns_empty(self):
        t = Trie()
        t.insert("test")
        assert t.starts_with("xyz") == []

    def test_case_insensitive(self):
        t = Trie()
        t.insert("Python")
        # Trie stores lowercased
        assert "python" in t.starts_with("py")
