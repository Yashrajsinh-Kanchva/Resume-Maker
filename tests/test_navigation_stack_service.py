"""Tests for services.navigation_stack_service."""
import pytest
from services.navigation_stack_service import open_view, go_back, current_view


class TestNavigationStackService:
    def test_initial_current_view_is_none(self):
        assert current_view() is None

    def test_open_view_and_current_view(self):
        open_view("dashboard")
        assert current_view() == "dashboard"
        open_view("settings")
        assert current_view() == "settings"

    def test_go_back_returns_previous_view(self):
        open_view("a")
        open_view("b")
        assert go_back() == "a"
        assert current_view() == "a"
        assert go_back() is None
        assert current_view() is None

    def test_go_back_on_empty(self):
        assert go_back() is None
