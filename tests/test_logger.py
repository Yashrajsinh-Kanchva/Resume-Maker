"""Tests for utils.logger."""
import pytest
import logging
import os
import tempfile
from utils.logger import setup_logger, LOG_DIR, MAX_LINES, LineRotatingFileHandler


def test_setup_logger_returns_logger():
    logger = setup_logger("TEST_LOGGER", "test_logger.log")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "TEST_LOGGER"


def test_setup_logger_idempotent():
    logger1 = setup_logger("IDEM", "idem.log")
    logger2 = setup_logger("IDEM", "idem.log")
    assert logger1 is logger2


def test_line_rotating_handler_init():
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        path = f.name
    try:
        handler = LineRotatingFileHandler(path, max_lines=10)
        assert handler.max_lines == 10
        assert handler.line_count >= 0
        handler.close()
    finally:
        if os.path.exists(path):
            try:
                os.unlink(path)
            except OSError:
                pass


def test_constants():
    assert LOG_DIR == "logs"
    assert MAX_LINES == 500
