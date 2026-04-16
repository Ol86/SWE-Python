"""Pydantic model for updating of member data."""

from datetime import date
from typing import Annotated, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

from library.entity.gender import Gender
from library.entity.member import Member
from library.router.constants import FIRST_NAME_PATTERN, LAST_NAME_PATTERN

__all__ = ["MemberUpdateModel"]


class MemberUpdateModel(BaseModel):
    """Model for updating member data using POST."""

    first_name: Annotated[
        str,
        StringConstraints(
            pattern=FIRST_NAME_PATTERN,
            max_length=64,
        ),
    ]
    """The first name."""

    last_name: Annotated[
        str,
        StringConstraints(
            pattern=LAST_NAME_PATTERN,
            max_length=64,
        ),
    ]
    """The last name."""

    gender: Gender
    """The gender."""

    date_of_birth: date
    """The date of birth."""

    member_since: date
    """The date since when the person is a member."""

    is_student: bool
    """Whether the member is a student."""

    email_address: EmailStr
    """Unique email address."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Test",
                "last_name": "Test",
                "gender": "D",
                "date_of_birth": "2026-03-31",
                "member_since": "2026-03-31",
                "is_student": False,
                "email_address": "test@acme.com",
            }
        }
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert the model to a dictionary.

        :return: Dictionary of the model
        :rtype: dict[str, Any]
        """
        new_dict: dict = self.model_dump()
        new_dict["id"] = None
        new_dict["username"] = None
        new_dict["address"] = None
        new_dict["books"] = []
        new_dict["interests"] = []
        new_dict["generated"] = None
        new_dict["updated"] = None

        return new_dict

    def to_member(self) -> Member:
        """Convert model to a member object.

        :return: Member object
        :rtype: Member
        """
        logger.debug("self={}", self)

        new_member_dict: dict = self.to_dict()
        new_member = Member(**new_member_dict)

        logger.debug("member={}", new_member)

        return new_member
