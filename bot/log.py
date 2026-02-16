"""
One-time logging setup for your bot.

Call `setup_logger()` once at startup (e.g. in your __init__.py) and then
just use `logging.getLogger(__name__)` everywhere else.
"""

import logging
import logging.handlers
import os
import warnings
from pathlib import Path

from rich.logging import RichHandler


def init_logging(
    *,
    level: int | str = logging.INFO,
    log_dir: str = "logs",
    log_file: str = "bot.log",
) -> None:
    """
    Configure the *root* logger once at application start.

    After this function runs you can simply do:
        import logging
        log = logging.getLogger(__name__)
        log.info("Hello, world!")
    """

    # Set the logging level
    level = os.environ.get("LOG_LEVEL", level)

    # Apparently this makes logging faster
    logging.logThreads = False
    logging.logProcesses = False
    logging.logMultiprocessing = False

    # Capture warnings
    warnings.simplefilter("always", DeprecationWarning)
    logging.captureWarnings(True)

    # Ensure log directory exists
    log_path: Path = Path(log_dir) / log_file
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Root logger configuration
    root: logging.Logger = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)

    # File handler: daily rotation, 7-day retention
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_path,
        when="midnight",
        utc=True,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    # Console handler: colourful Rich output
    console_handler = RichHandler(
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )

    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[file_handler, console_handler],
    )

    root.info(
        "Logging configured (level=%s, file=%s)",
        logging.getLevelName(root.level),
        log_path,
    )


if __name__ == "__main__":
    init_logging()

    log = logging.getLogger(__name__)
    log.debug("This is a debug message")
    log.info("This is an info message")
    log.warning("This is a warning message")
    log.error("This is an error message")
    log.critical("This is a critical message")
