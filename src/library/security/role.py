"""Enum fr roles."""

from enum import StrEnum


class Role(StrEnum):
    """Enum for roles."""

    ADMIN = "ADMIN"
    """Role for admins."""

    PATIENT = "PATIENT"
    """Role for patients."""
