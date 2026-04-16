"""The module provides the database configuration for the application."""

from importlib.resources import files
from typing import TYPE_CHECKING, Final, Literal

from loguru import logger
from sqlalchemy.engine import URL

from library.config.config import app_config, resources_path

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable

__all__: list[str] = [
    "db_connect_args",
    "db_dialect",
    "db_log_statements",
    "db_url",
    "db_url_admin",
]

_db_toml: Final = app_config.get("db", {})

db_dialect: Final[Literal["postgresql"]] = _db_toml.get(
    "dialect",
    "postgresql",
)

logger.debug("db: dialect={}", db_dialect)

_drivername: Final[str] = "postgresql+psycopg"
_db_name: Final[str] = _db_toml.get("name", "library")
_db_host: Final[str] = _db_toml.get("host", "postgres")
_db_user: Final[str] = _db_toml.get("user", "library")
_db_password: Final[str] = _db_toml.get("password", "Change Me!")
_db_password_admin: Final[str] = _db_toml.get("password", "Change Me!")

db_log_statements: Final[bool] = bool(_db_toml.get("log_statements", False))

db_url: Final[URL] = URL.create(
    drivername=_drivername,
    username=_db_user,
    password=_db_password,
    host=_db_host,
    database=_db_name,
)

logger.debug("db: url={}", db_url)

db_url_admin: Final[URL] = URL.create(
    drivername=_drivername,
    username="postgres",
    password=_db_password_admin,
    host=_db_host,
    database=_db_name,
)


def _create_connect_args() -> dict[str, str | dict[str, str]] | None:
    """Create the connect args for the database connection."""
    db_resources_traversable: Final[Traversable] = files(resources_path)

    cafile: Final = str(db_resources_traversable / db_dialect / "server.crt")

    return {
        "sslmode": "verify-full",
        "sslrootcert": cafile,
    }


db_connect_args: dict[str, str | dict[str, str]] | None = _create_connect_args()

logger.debug("db: connect_args={}", db_connect_args)
