import logging
import os
import pytest
from pathlib import Path
from services.logger import setup_logging
from config import LOG_DIR, LOG_MAX_BYTES, LOG_BACKUP_COUNT


def _close_handlers(logger: logging.Logger):
    """Close all handlers and clear them so file locks are released."""
    for h in logger.handlers:
        h.close()
    logger.handlers.clear()


def test_setup_logging_creates_file():
    logger = setup_logging("test_bot")
    assert logger is not None
    assert logger.level == logging.INFO
    log_file = Path(LOG_DIR) / "test_bot.log"
    assert log_file.exists(), f"Log file {log_file} was not created"
    logger.info("test message")
    _close_handlers(logger)
    log_file.unlink(missing_ok=True)


def test_logger_not_duplicate_handlers():
    logger = setup_logging("test_dedup")
    count_before = len(logger.handlers)
    logger2 = setup_logging("test_dedup")
    assert len(logger2.handlers) == count_before
    _close_handlers(logger)
    log_file = Path(LOG_DIR) / "test_dedup.log"
    log_file.unlink(missing_ok=True)


def test_logger_writes_to_file():
    logger = setup_logging("test_write")
    test_msg = "hello from test"
    logger.info(test_msg)
    log_file = Path(LOG_DIR) / "test_write.log"
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert test_msg in content
    _close_handlers(logger)
    log_file.unlink(missing_ok=True)


def test_logger_levels():
    logger = setup_logging("test_levels")
    assert logger.isEnabledFor(logging.INFO)
    assert logger.isEnabledFor(logging.WARNING)
    assert logger.isEnabledFor(logging.ERROR)
    assert not logger.isEnabledFor(logging.DEBUG)
    _close_handlers(logger)
    log_file = Path(LOG_DIR) / "test_levels.log"
    log_file.unlink(missing_ok=True)


def test_logger_config_constants():
    assert LOG_MAX_BYTES == 5 * 1024 * 1024
    assert LOG_BACKUP_COUNT >= 1
