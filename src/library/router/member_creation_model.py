"""Pydantic model for member data needed for creating a new member."""

from typing import Annotated, Final

from loguru import logger
from pydantic import StringConstraints

from library.entity.genre import Genre
from library.entity.member import Member
from library.router.address_model import AddressModel
from library.router.book_model import BookModel
from library.router.member_update_model import MemberUpdateModel


class MemberCreationModel(MemberUpdateModel):
    """Model for member data for POST."""

    username: Annotated[str, StringConstraints(max_length=20)]
    """Username for login."""

    address: AddressModel
    """Adress of member."""

    books: list[BookModel]
    """List with borrowed books."""

    interests: list[Genre]
    """List of genre interests."""

    def to_member(self) -> Member:
        """Covert the model to a Member object.

        :return: member object
        :rtype: Member
        """
        logger.debug("self={}", self)

        new_member_dict: dict = self.to_dict()
        new_member_dict["username"] = self.username
        new_member_dict["interests"] = self.interests

        new_member: Final = Member(**new_member_dict)
        new_member.address = self.address.to_address()
        new_member.books = [book_model.to_book() for book_model in self.books]

        logger.debug("member={}", new_member)

        return new_member
