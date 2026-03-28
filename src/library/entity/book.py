"""Entity class for a book borrowed by a library member"""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from library.entity.base import Base
from library.entity.genre import Genre
from library.entity.member import Member


class Book(Base):
    """Entity class for borrowed books"""

    __tablename__ = "book"

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Generated ID, starting at 1000"""

    name: Mapped[str]
    """Name of the book"""

    author: Mapped[str | None]
    """Full name of the author"""

    still_borrowed: Mapped[bool | None]
    """Boolean, wether the member has already returned the borrowed book"""

    genre: Mapped[Genre | None]
    """Transient list of genres as enums"""

    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    """ID of member that has borrowed this book as a foreign key"""

    member: Mapped[Member] = relationship(back_populates="books")
    """Transient Member object"""

    def __repr__(self) -> str:
        """Book data as a string without member data"""
        return (
            f"Book(id={self.id}, "
            + f"name={self.name}, "
            + f"author={self.author})"
            + f"is_returned={self.still_borrowed}"
            + f"genre={self.genre})"
        )
