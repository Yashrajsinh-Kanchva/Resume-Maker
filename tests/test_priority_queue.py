"""Tests for DS.priority_queue."""
import pytest
from DS.priority_queue import PriorityQueue


class TestPriorityQueue:
    def test_push_pop_max_first(self):
        pq = PriorityQueue()
        pq.push((3, "c"))
        pq.push((1, "a"))
        pq.push((2, "b"))
        assert pq.pop() == (3, "c")
        assert pq.pop() == (2, "b")
        assert pq.pop() == (1, "a")
        assert pq.pop() is None

    def test_empty_pop(self):
        pq = PriorityQueue()
        assert pq.pop() is None

    def test_is_empty(self):
        pq = PriorityQueue()
        assert pq.is_empty() is True
        pq.push((1, "x"))
        assert pq.is_empty() is False
        pq.pop()
        assert pq.is_empty() is True

    def test_single_element(self):
        pq = PriorityQueue()
        pq.push((10, "only"))
        assert pq.pop() == (10, "only")
        assert pq.is_empty() is True
