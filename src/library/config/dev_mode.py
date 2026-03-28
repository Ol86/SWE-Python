"""The module contains configuration values for the development mode, e.g. whether to use mock data or not."""

from typing import Final

from library.config.config import app_config

_dev_toml: Final = app_config.get("dev", {})
