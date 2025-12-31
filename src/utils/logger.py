"""Logging utilities for the app.

Provides `init_logger` to configure root logging handlers (console + rotating
file) and `get_logger` to obtain a `LoggerAdapter` that includes a
`session_uid` in log records.
"""
from __future__ import annotations

import logging
import os
from logging import Logger
from logging.handlers import RotatingFileHandler
from typing import Optional


class SessionFilter(logging.Filter):
    """Ensure `session_uid` attribute exists on log records."""

    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover - trivial
        if not hasattr(record, "session_uid"):
            record.session_uid = "-"
        return True


def init_logger(
    level: Optional[str] = None,
    log_dir: str = "logs",
    filename: str = "app.log",
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    to_stdout: bool = True,
) -> None:
    """Initialize root logger with rotating file and optional console handler.

    Environment variables respected when parameters are not provided:
    - LOG_LEVEL
    - LOG_DIR
    """
    level = level or os.getenv("LOG_LEVEL", "INFO")
    log_dir = os.getenv("LOG_DIR", log_dir)
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    root = logging.getLogger()
    # Avoid adding handlers multiple times in interactive/dev reloads
    if getattr(root, "__custom_logger_initialized__", False):
        return

    root.setLevel(numeric_level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(session_uid)s] %(name)s: %(message)s"
    )

    os.makedirs(log_dir, exist_ok=True)
    fh = RotatingFileHandler(
        os.path.join(log_dir, filename), maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    fh.setLevel(numeric_level)
    fh.setFormatter(formatter)
    fh.addFilter(SessionFilter())
    root.addHandler(fh)

    if to_stdout:
        ch = logging.StreamHandler()
        ch.setLevel(numeric_level)
        ch.setFormatter(formatter)
        ch.addFilter(SessionFilter())
        root.addHandler(ch)

    logging.captureWarnings(True)
    setattr(root, "__custom_logger_initialized__", True)


def get_logger(name: str, session_uid: Optional[str] = None) -> logging.LoggerAdapter:
    """Return a LoggerAdapter that injects `session_uid` into log records.

    If `session_uid` is not provided, the adapter will use `-` as placeholder.
    """
    base: Logger = logging.getLogger(name)
    extra = {"session_uid": session_uid or "-"}
    return logging.LoggerAdapter(base, extra)
