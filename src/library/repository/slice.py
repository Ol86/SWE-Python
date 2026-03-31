"""The module provides a slice class for paginated results."""

from dataclasses import dataclass
from typing import TypeVar

__all__: list[str] = ["Slice"]

T = TypeVar("T")


@dataclass(eq=False, slots=True, kw_only=False)
class Slice[T]:
    """Represents a slice of paginated results."""

    content: tuple[T, ...]
    """The content of the slice."""

    total_elements: int
    """The total number of elements in the result set."""
