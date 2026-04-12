"""Page utility functions for handling paginated responses."""

from dataclasses import dataclass
from math import ceil
from typing import Any, Final

from library.repository import Pageable

__all__: list[str] = ["Page"]


@dataclass(eq=False, slots=True, kw_only=True)
class PageMeta:
    """Metadata for a paginated response."""

    size: int
    """Number of items per page."""

    number: int
    """Current page number (0-based)."""

    total_elements: int
    """Total number of elements across all pages."""

    total_pages: int
    """Total number of pages."""


@dataclass(eq=False, slots=True, kw_only=True)
class Page:
    """A paginated response containing content and metadata."""

    content: tuple[dict[str, Any], ...]
    """The content of the current page as a tuple of dictionaries."""

    page: PageMeta
    """Metadata for the paginated response."""

    @staticmethod
    def create(
        content: tuple[dict[str, Any], ...],
        pageable: Pageable,
        total_elements: int,
    ) -> Page:
        """Create a Page object from content, pagination information, and total elements.

        :param content: The content of the current page as a tuple of dictionaries.
        :param pageable: The Pageable object containing pagination information.
        :param total_elements: The total number of elements across all pages.
        :return: A Page object containing the content and metadata.
        :rtype: Page
        """
        total_pages: Final = ceil(total_elements / pageable.size)
        page_meta = PageMeta(
            size=pageable.size,
            number=pageable.number,
            total_elements=total_elements,
            total_pages=total_pages,
        )
        return Page(content=content, page=page_meta)
