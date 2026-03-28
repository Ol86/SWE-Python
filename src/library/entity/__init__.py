"""
This package holds all entities.
"""

from library.entity.address import Address
from library.entity.book import Book
from library.entity.member import Member

__all__: list[str] = ["Member", "Book", "Address"]
