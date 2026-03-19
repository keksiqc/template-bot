"""
One-time logging setup for your bot.

Call `init_logging()` once at startup (e.g. in your __init__.py) and then
just use `logging.getLogger(__name__)` everywhere else.
"""

from __future__ import annotations

import logging
import logging.handlers
import os
from pathlib import Path


try:
    from colorlog import ColoredFormatter
except ImportError:
    ColoredFormatter = None


DEFAULT_LOG_PATH = Path("logs/bot.log")
FILE_LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
CONSOLE_LOG_FORMAT = (
    "%(thin)s%(asctime)s%(reset)s %(log_color)s%(levelname)-8s%(reset)s [%(thin_blue)s%(name)s%(reset)s] %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _build_file_handler(log_path: Path) -> logging.Handler:
    """Create the rotating file handler used for persistent logs."""

    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_path,
        when="midnight",
        utc=True,
        backupCount=7,
        encoding="utf-8",
        delay=True,
    )
    file_handler.setFormatter(logging.Formatter(fmt=FILE_LOG_FORMAT, datefmt=DATE_FORMAT))
    return file_handler


def _build_stream_handler() -> logging.Handler:
    """Create the console handler, using color when available."""

    stream_handler = logging.StreamHandler()

    if ColoredFormatter is None:
        stream_handler.setFormatter(logging.Formatter(fmt=FILE_LOG_FORMAT, datefmt=DATE_FORMAT))
        return stream_handler

    stream_handler.setFormatter(ColoredFormatter(fmt=CONSOLE_LOG_FORMAT, datefmt=DATE_FORMAT))
    return stream_handler


def init_logging(
    *,
    level: int | str = logging.INFO,
    log_path: str | Path = DEFAULT_LOG_PATH,
) -> None:
    """Configure the root logger once at application start."""

    resolved_log_path = Path(log_path)
    resolved_level = os.environ.get("LOG_LEVEL", level)

    # Skip per-record thread/process bookkeeping unless you need it in the format string.
    logging.logThreads = False
    logging.logProcesses = False
    logging.logMultiprocessing = False

    logging.captureWarnings(True)

    resolved_log_path.parent.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.handlers.clear()

    root.setLevel(resolved_level)

    root.addHandler(_build_file_handler(resolved_log_path))
    root.addHandler(_build_stream_handler())
    root.info(
        "Logging configured",
        extra={
            "log_level_name": logging.getLevelName(root.level),
            "log_path": str(resolved_log_path),
        },
    )


def _run_self_test() -> None:
    """Emit one message at each severity to validate the logger configuration."""

    init_logging(level="DEBUG")
    log = logging.getLogger(__name__)

    log.debug("Debug self-test message")
    log.info("Info self-test message")
    log.warning("Warning self-test message")
    log.error("Error self-test message")
    log.critical("Critical self-test message")


if __name__ == "__main__":
    _run_self_test()
