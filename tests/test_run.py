"""Tests for run module (app entry point)."""
import sys
from unittest.mock import patch


def test_run_module_has_app():
    """Importing run creates app via create_app()."""
    import run as run_mod
    assert hasattr(run_mod, "app")
    assert run_mod.app is not None
