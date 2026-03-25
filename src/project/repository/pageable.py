"""
Pageable data class.
"""

from dataclasses import dataclass
from typing import Final

__all__ = [
    "MAX_PAGE_SIZE",
    "Pageable",
]


DEFAULT_PAGE_SIZE: Final = 5
MAX_PAGE_SIZE: Final = 100
DEFAULT_PAGE_NUMBER: Final = 0


@dataclass(eq=False, slots=True, kw_only=True)
class Pageable:
    """
    Pageable data class.
    """

    size: int
    """
    Page size.
    """

    number: int
    """
    Page number.
    """

    @staticmethod
    def create(number: str | None = None, size: str | None = None) -> Pageable:  # noqa F821
        """
        Create a Pageable instance.

        :param number: Page number as a string.
        :param size: Page size as a string.
        :return: Pageable instance with the given page number and size.
        :rtype: Pageable
        """
        number_int: Final = (
            DEFAULT_PAGE_NUMBER
            if number is None or not number.isdigit()
            else int(number)
        )
        size_int: Final = (
            DEFAULT_PAGE_SIZE
            if size is None
            or not size.isdigit()
            or int(size) > MAX_PAGE_SIZE
            or int(size) < 0
            else int(size)
        )
        return Pageable(size=size_int, number=number_int)
