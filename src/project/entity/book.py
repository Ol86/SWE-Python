"""Entity class for a book borrowed by a library member"""

from dataclasses import InitVar

from loguru import logger
from sqlalchemy import ForeignKey, JSON, Identity
from sqlalchemy.orm import Mapped, mapped_column, reconstructor, relationship

from project.entity.base import Base
from project.entity.genre import Genre
from project.entity.member import Member

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

    is_returned: Mapped[bool | None] #TODO Sinnvoll?
    """Boolean, wether the member has already returned the borrowed book"""

    genres: InitVar[list[Genre] | None] #TODO Sinnvoll als Liste? Notwendig?
    """Transient list of genres as enums"""

    genres_json: Mapped[list[str] | None] = mapped_column(
        JSON,
        name="genres",
        init=False
    )
    """Persistent list of genres for a JSON array"""

    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    """ID of member that has borrowed this book as a foreign key"""

    member: Mapped[Member] = relationship(
        back_populates="books"
    )
    """Transient Member object"""

    def __post_init__(self, genres: list[Genre] | None,) -> None: #TODO Sinnvoll?
        """Sets JSON array for database INSERT or UPDATE
        
        :param genres: List with genres as enum
        """
        logger.debug("genres={}", genres)
        logger.debug("self={}", self)
        
        self.genres_json = (
            [genre_enum.name for genre_enum in genres]
            if genres is not None
            else None
        )
        logger.debug("self.genres_json={}", self.genres_json)


    @reconstructor
    def on_load(self) -> None: #TODO Sinnvoll?
        """Initialises Enum list through the database strings"""

        self.genres = (
            [Genre[genre_name] for genre_name in self.genres_json]
            if self.genres_json is not None
            else []
        )
        logger.debug("genres={}", self.genres,)


    def __repr__(self) -> str:
        """Book data as a string without member data"""
        return (
            f"Book(id={self.id}, "
            + f"name={self.name}, "
            + f"author={self.author})"
            + f"is_returned={self.is_returned}"
            + f"genres_json={self.genres_json})"
        )

