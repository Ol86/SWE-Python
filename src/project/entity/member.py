"""Entity class for a library member"""

from dataclasses import InitVar
from datetime import date, datetime
from typing import Any, Self

#from loguru import logger #TODO Logging
from sqlalchemy import Identity, func 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.entity.address import Address
from project.entity.base import Base
from project.entity.book import Book
from project.entity.gender import Gender
from project.entity.genre import Genre

#TODO Strawberry
class Member(Base):
    """Entity class for a library member"""

    __tablename__ = "member"
    """Tablename for sqlalchemy"""

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True
    )
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

    interests: InitVar[list[Genre] | None] #TODO Sinnvoll hier? Sinnvoll in books?
    #TODO Wenn sinnvoll, interests_json, __post_init__ und on_load

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

    generated: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None
    )
    """Timestamp of initial INSERT into the database"""

    updated: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None
    )
    """Timestamp of the last UPDATE in the database"""

    def set(self, member: Self) -> None:
        """Overwrite primitive attributes
        
        :param member: Member object
        """

        self.first_name = member.first_name
        self.last_name = member.last_name
        self.date_of_birth = member.date_of_birth
        self.email = member.email

    
    def __eq__(self, other: Any) -> bool:
        """Compares two Members without using joins.
        
        :param other: Object for comparison
        """

        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False

        return self.id is not None and self.id == other.id
    

    def __hash__(self) -> int:
        """Returns Hash using ID without joins."""
        return hash(self.id) if self.id is not None else hash(type(self))


    def __repr__(self) -> str:
        """Member data as a string without using joins"""

        return (
            f"Member(id={self.id}, "
            + f"first_name={self.first_name}, "
            + f"last_name={self.last_name}, "
            #TODO Other attributes
            + ")"
        )











    
