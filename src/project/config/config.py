"""
This module provides the configuration for the application.
It loads the configuration from a TOML file and makes it available as a dictionary.
The configuration file is located in the resources directory of the project.
The module also defines a constant for the path to the resources directory.
"""

from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from tomllib import load
from typing import Any, Final

from loguru import logger

__all__ = ["app_config", "resources_path"]


resources_path: Final[str] = "project.config.resources"

_resources_traversable: Final[Traversable] = files(resources_path)
_config_file: Final[Traversable] = _resources_traversable / "app.toml"
logger.debug("config: _config_file={}", _config_file)


with Path(str(_config_file)).open(mode="rb") as reader:
    app_config: Final[dict[str, Any]] = load(reader)
    logger.debug("config: app_config={}", app_config)
