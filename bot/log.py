"""
One-time logging setup for your bot.

Call `setup_logger()` once at startup (e.g. in your __init__.py) and then
just use `logging.getLogger(__name__)` everywhere else.
"""

import logging
import logging.handlers
from pathlib import Path

from rich.logging import RichHandler


def setup_logger(
    *,
    level: str | int = logging.INFO,
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
    numeric_level = level if isinstance(level, int) else logging.getLevelName(level.upper())

    # Ensure log directory exists
    log_path: Path = Path(log_dir) / log_file
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Root logger configuration
    root: logging.Logger = logging.getLogger()
    root.setLevel(numeric_level)
    # Remove any default handlers
    root.handlers.clear()

    # File handler: daily rotation, 14-day retention
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_path,
        when="midnight",
        utc=True,
        backupCount=14,
        encoding="utf-8",
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root.addHandler(file_handler)

    # Console handler: colourful Rich output
    console_handler = RichHandler(
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )
    root.addHandler(console_handler)

    root.info(
        "Logging configured (level=%s, file=%s)",
        logging.getLevelName(numeric_level),
        log_path,
    )


if __name__ == "__main__":
    setup_logger()
