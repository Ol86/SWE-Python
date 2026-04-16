"""The module contains configuration values for the development mode, e.g. whether to use mock data or not."""

from typing import Final

from library.config.config import app_config

__all__: list[str] = ["dev_db_populate", "dev_keycloak_populate"]

_dev_toml: Final = app_config.get("dev", {})

dev_db_populate: Final[bool] = bool(_dev_toml.get("db-populate", False))

dev_keycloak_populate: Final[bool] = bool(_dev_toml.get("keycloak-populate", False))
