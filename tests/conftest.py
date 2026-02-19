"""Pytest fixtures."""
import os
# Allow tests to run without real DB/Redis/OpenAI (CI and local)
os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
os.environ.setdefault("OPENAI_API_KEY", "sk-dummy")

import pytest


@pytest.fixture(autouse=True)
def reset_nav_stack():
    """Reset navigation stack before each test that uses it."""
    import services.navigation_stack_service as nav_mod
    from DS.stack import Stack
    nav_mod._nav_stack = Stack()
    yield
    nav_mod._nav_stack = Stack()
