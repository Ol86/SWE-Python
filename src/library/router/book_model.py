"""Pydantic model for a book."""

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, StringConstraints

from library.entity.book import Book
from library.entity.genre import Genre
from library.router.constants import ISBN_PATTERN


class BookModel(BaseModel):
    """Model for a borrowed book."""

    name: str
    """The book's name."""

    isbn: Annotated[str, StringConstraints(pattern=ISBN_PATTERN, max_length=17)]
    """The ISBN number of the book."""

    author: str | None = None
    """The book's author."""

    still_borrowed: bool | None = None
    """Is the book still borrowed?"""

    genre: Genre
    """Genre of the book."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Testbook",
                "isbn": "978-3-16-148410-0",
                "author": "Test Author",
                "still_borrowed": True,
                "genre": "S",
            },
        }
    )

    def _to_dict(self) -> dict[str, Any]:
        """Convert model into a dictionary.

        :return: book dictionary
        :rtype: dict[str, Any]
        """
        new_dict: dict = self.model_dump()
        new_dict["id"] = None
        new_dict["member_id"] = None
        new_dict["member"] = None

        return new_dict

    def to_book(self) -> Book:
        """Convert model into a book object.

        :return: book object
        :rtype: Book
        """
        book_dict: dict = self._to_dict()

        return Book(**book_dict)
