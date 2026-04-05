"""Enum fr roles."""

from enum import StrEnum


class Role(StrEnum):
    """Enum for roles."""

    ADMIN = "ADMIN"
    """Role for admins."""

    MEMBER = "MEMBER"
    """Role for members."""
