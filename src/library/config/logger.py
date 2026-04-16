"""The configuration module for logging settings in the application."""

from pathlib import Path
from typing import Final

from loguru import logger

__all__: list[str] = ["config_logger"]

LOG_FILE: Final = Path("log") / "app.log"


def config_logger() -> None:
    """Configure the logger to write logs to a file with rotation and retention settings."""
    logger.add(LOG_FILE, rotation="1 MB")
