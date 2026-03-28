"""Entity class for a library member."""

from dataclasses import InitVar
from datetime import date, datetime
from typing import Any, Self

from loguru import logger
from sqlalchemy import JSON, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, reconstructor, relationship

from library.entity.address import Address
from library.entity.base import Base
from library.entity.book import Book
from library.entity.gender import Gender
from library.entity.genre import Genre


# TODO Strawberry
class Member(Base):
    """Entity class for a library member."""

    __tablename__ = "member"
    """Tablename for sqlalchemy"""

    id: Mapped[int | None] = mapped_column(Identity(start=1000), primary_key=True)
    """ID starting at 1000 for testing purposes"""

    last_name: Mapped[str]
    """Family name of member"""

    first_name: Mapped[str]
    """First name of member"""

    gender: Mapped[Gender | None]
    """Gender of the member"""

    date_of_birth: Mapped[date]
    """Date of birth of the member"""

    member_since: Mapped[date | None]
    """Since when the person is a member in the library.
    Is resetted after leaving and joining again."""

    is_student: Mapped[bool | None]
    """Member's student status due to discount"""

    email_address: Mapped[str] = mapped_column(unique=True)
    """Unique email address"""

    interests: InitVar[list[Genre] | None]
    """Tansient list of genre interests of the member"""

    interests_json: Mapped[list[str] | None] = mapped_column(JSON, name="genres", init=False)
    """Persistent list of genres for a JSON array"""

    address: Mapped[Address] = relationship(
        back_populates="member",
        cascade="save-update, delete",
    )
    """Member's address (1:1 relationship)"""

    books: Mapped[Book] = relationship(
        back_populates="member",
        cascade="save-update, delete",
    )
    """Books currently borrowed by the member (1:N relationship)"""

    version: Mapped[int] = mapped_column(nullable=False, default=0)
    """Version number for prevention of lost updates"""

    generated: Mapped[datetime | None] = mapped_column(insert_default=func.now(), default=None)
    """Timestamp of initial INSERT into the database"""

    updated: Mapped[datetime | None] = mapped_column(insert_default=func.now(), onupdate=func.now(), default=None)
    """Timestamp of the last UPDATE in the database"""

    def __post_init__(
        self,
        genres: list[Genre] | None,
    ) -> None:
        """Set JSON array for database INSERT or UPDATE.

        :param genres: List with genres as enum
        """
        logger.debug("genres={}", genres)
        logger.debug("self={}", self)

        self.interests_json = [genre_enum.name for genre_enum in genres] if genres is not None else None
        logger.debug("self.genres_json={}", self.interests_json)

    @reconstructor
    def on_load(self) -> None:
        """Initialise Enum list through the database strings."""
        self.interests = [Genre[genre_name] for genre_name in self.interests_json] if self.interests_json is not None else []
        logger.debug(
            "interests={}",
            self.interests,
        )

    def set(self, member: Self) -> None:
        """Overwrite primitive attributes.

        :param member: Member object
        """
        self.first_name = member.first_name
        self.last_name = member.last_name
        self.date_of_birth = member.date_of_birth
        self.email = member.email

    def __eq__(self, other: Any) -> bool:
        """Compare two Members without using joins.

        :param other: Object for comparison
        """
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False

        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Return Hash using ID without joins."""
        return hash(self.id) if self.id is not None else hash(type(self))

    def __repr__(self) -> str:
        """Member data as a string without using joins."""
        return (
            f"Member(id={self.id}, "
            + f"first_name={self.first_name}, "
            + f"last_name={self.last_name}, "
            + f"gender={self.gender}, "
            + f"date_of_birth={self.date_of_birth}, "
            + f"member_since={self.member_since}, "
            + f"is_student={self.is_student}, "
            + f"email_address={self.email_address}, "
            + f"interests_json={self.interests_json}, "
            + f"generated={self.generated}, "
            + f"updated={self.updated}"
            + ")"
        )
