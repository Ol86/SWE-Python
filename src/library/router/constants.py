"""Constants for models etc."""

from typing import Final

__all__ = [
    "ETAG",
    "IF_MATCH",
    "IF_MATCH_MIN_LEN",
    "IF_NONE_MATCH",
    "IF_NONE_MATCH_MIN_LEN",
]

ETAG: Final = "ETag"
IF_MATCH: Final = "if-match"
IF_MATCH_MIN_LEN: Final = 3
IF_NONE_MATCH: Final = "if-none-match"
IF_NONE_MATCH_MIN_LEN: Final = 3

LAST_NAME_PATTERN: Final = r"^(?:(?:[vV]on|[vV]an|[zZ]u|[dD]e|[dD]el|[dD]er)\s)*[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)*$"
"""Regex pattern for last names. It allows multiple names and noble names."""

FIRST_NAME_PATTERN: Final = r"^(?:[A-ZÄÖÜ][a-zäöüß]+)(?:[ -][A-ZÄÖÜ][a-zäöüß]+)*$"
"""Regex pattern for first names. Allows multiple names."""

POSTAL_CODE_PATTERN: Final = r"^\d{5}$"
"""Regex pattern for German postal codes."""

PLACE_PATTERN: Final = (
    r"^(?:[A-ZÄÖÜ][a-zäöüß]+)(?:[ -][A-ZÄÖÜ][a-zäöüß]+)*(?:\s(?:am|an der|an den|im|in der|bei)\s[A-ZÄÖÜ][a-zäöüß]+"
    + r"(?:[ -][A-ZÄÖÜ][a-zäöüß]+)*)?$"
)
"""Regex pattern for place names."""

AUTHOR_PATTERN: Final = (
    r"^(?:[A-ZÄÖÜ][a-zäöüß]+(?:[- ][A-ZÄÖÜ][a-zäöüß]+)*)\s(?:[vV]on\s|[vV]an\s|[zZ]u\s|[dD]e\s|[dD]el\s|[dD]er\s)?"
    + r"[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)*$"
)
"""Regex pattern for an author's name."""

ISBN_PATTERN: Final = r"^(97[89])-\d{1,5}-\d{1,7}-\d{1,7}-\d$"
"""Regex pattern for ISBN13."""
