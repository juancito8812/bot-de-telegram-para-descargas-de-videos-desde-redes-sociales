import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import LOG_DIR, LOG_LEVEL, LOG_MAX_BYTES, LOG_BACKUP_COUNT


def setup_logging(name: str = "bot") -> logging.Logger:
    """Configure and return a logger with rotating file handler + console.

    File:  ``{LOG_DIR}/{name}.log``, rotated at *LOG_MAX_BYTES*,
           keeping *LOG_BACKUP_COUNT* backups.
    Console: stderr, same format, no buffering.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Avoid duplicate handlers when setup_logging is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-7s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Rotating file handler ──────────────────
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        filename=log_dir / f"{name}.log",
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # ── Console handler (stderr) ───────────────
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
