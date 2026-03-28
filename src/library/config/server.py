"""The module contains configuration values for the server, e.g. host binding and port.

The values are read from the `app_config` dictionary, which is defined in the `config`
module and populated from the `config.toml` file.
"""

from typing import Final

from library.config.config import app_config

__all__ = ["host_binding", "port"]


_server_toml: Final = app_config.get("server", {})

host_binding: Final[str] = _server_toml.get("host-binding", "127.0.0.1")
"""'Host binding', z.B. 127.0.0.1 (default) oder 0.0.0.0."""

port: Final[int] = _server_toml.get("port", 8000)
"""Port for the server (default: 8000)."""

reload: Final[bool] = bool(_server_toml.get("reload", False))
