"""Tests for DS.stack."""
import pytest
from DS.stack import Stack


class TestStack:
    def test_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1
        assert s.pop() is None

    def test_peek(self):
        s = Stack()
        assert s.peek() is None
        s.push("a")
        assert s.peek() == "a"
        s.push("b")
        assert s.peek() == "b"
        s.pop()
        assert s.peek() == "a"

    def test_is_empty(self):
        s = Stack()
        assert s.is_empty() is True
        s.push(1)
        assert s.is_empty() is False
        s.pop()
        assert s.is_empty() is True

    def test_size(self):
        s = Stack()
        assert s.size() == 0
        s.push(1)
        s.push(2)
        assert s.size() == 2
        s.pop()
        assert s.size() == 1
