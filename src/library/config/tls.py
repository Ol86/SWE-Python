"""
This module provides the TLS configuration for the SWE API.
It reads the TLS configuration from the application configuration and sets up the paths to the TLS certificate and key files.
The TLS configuration is used to enable secure communication between the server and clients.
"""

from importlib.resources import files
from typing import TYPE_CHECKING, Final

from loguru import logger

from library.config.config import app_config, resources_path

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable

__all__ = ["tls_certfile", "tls_keyfile"]


_tls_toml: Final = app_config.get("tls", {})
_tls_path: Final[Traversable] = files(resources_path) / "tls"

_key: Final[str] = _tls_toml.get("key", "key.pem")
tls_keyfile: Final[str] = str(_tls_path / _key)
logger.debug("private keyfile TLS: {}", tls_keyfile)

_certificate: Final[str] = _tls_toml.get("certificate", "certificate.crt")
tls_certfile: Final[str] = str(_tls_path / _certificate)
logger.debug("certfile TLS: {}", tls_certfile)
