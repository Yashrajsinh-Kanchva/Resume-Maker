"""Tests for DS.hashmap."""
import pytest
from DS.hashmap import HashMap


class TestHashMap:
    def test_put_and_get_map(self):
        h = HashMap()
        h.put("Python")
        h.put("python")
        assert h.get_map() == {"python": 2}

    def test_put_all(self):
        h = HashMap()
        h.put_all(["a", "b", "a", "c", "b", "a"])
        assert h.get_map() == {"a": 3, "b": 2, "c": 1}

    def test_empty(self):
        h = HashMap()
        assert h.get_map() == {}

    def test_case_insensitive(self):
        h = HashMap()
        h.put("Java")
        h.put("JAVA")
        assert h.get_map() == {"java": 2}
