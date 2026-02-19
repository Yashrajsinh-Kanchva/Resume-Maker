"""Pytest fixtures."""
import pytest


@pytest.fixture(autouse=True)
def reset_nav_stack():
    """Reset navigation stack before each test that uses it."""
    import services.navigation_stack_service as nav_mod
    from DS.stack import Stack
    nav_mod._nav_stack = Stack()
    yield
    nav_mod._nav_stack = Stack()
