"""Configuration for mail server."""

from typing import Final

from patient.config.config import app_config

__all__ = ["mail_enabled", "mail_host", "mail_port", "mail_timeout"]


_mail_toml: Final = app_config.get("mail", {})

mail_enabled: Final = bool(_mail_toml.get("enabled", True))
"""True, if mail server is active."""

mail_host: Final[str] = _mail_toml.get("host", "mail")
"""Name of the mail server."""

mail_port: Final[int] = _mail_toml.get("port", 25)
"""Port of the mail server."""

mail_timeout: Final[float] = _mail_toml.get("timeout", 1.0)
"""Timeout for the mail server in seconds."""
