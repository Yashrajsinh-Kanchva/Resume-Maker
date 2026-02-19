"""Tests for config.db."""
import pytest
from config.db import get_users_collection, get_feedback_collection


def test_get_users_collection_returns_collection():
    coll = get_users_collection()
    assert coll is not None


def test_get_feedback_collection_returns_collection():
    coll = get_feedback_collection()
    assert coll is not None
