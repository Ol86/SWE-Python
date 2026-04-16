"""The Enum for book genres."""

from enum import StrEnum

import strawberry


@strawberry.enum
class Genre(StrEnum):
    """Selection of possible genres (incomplete)."""

    FANTASY = "F"
    """For Fantasy Books"""

    SCIENCE_FICTION = "S"
    """For SciFi Books"""

    CRIME_NOVEL = "C"
    """For Crime Novels"""

    THRILLER = "T"
    """For Thrillers"""

    NON_FICTION = "N"
    """For Non-fictional books"""
