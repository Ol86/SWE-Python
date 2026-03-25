"""
This module handles the database repository for the project.
"""

from project.repository.pageable import MAX_PAGE_SIZE, Pageable

__all__: list[str] = [
    "MAX_PAGE_SIZE",
    "Pageable",
]
