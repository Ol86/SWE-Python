"""Data Transfer Object class for member data."""

from dataclasses import dataclass
from datetime import date

from library.entity import Member
from library.entity.gender import Gender
from library.entity.genre import Genre
from library.service.address_dto import AddressDTO

__all__ = ["MemberDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
# TODO Strawberry
class MemberDTO:
    """DTO class for read or saved member data."""

    id: int
    version: int
    first_name: str
    last_name: str
    username: str
    gender: Gender | None
    date_of_birth: date
    member_since: date | None
    is_student: bool | None
    email_address: str
    interests: list[Genre]
    address: AddressDTO

    def __init__(self, member: Member):
        """Initialize MemberDTO using Member object.

        :param member: Member object
        """
        member_id: int | None = member.id
        self.id = member_id if member_id is not None else -1
        self.version = member.version
        self.first_name = member.first_name
        self.last_name = member.last_name
        self.username = member.username
        self.gender = member.gender
        self.date_of_birth = member.date_of_birth
        self.member_since = member.member_since
        self.is_student = member.is_student
        self.email_address = member.email_address
        self.interests = [Genre[genre] for genre in member.interests_json] if member.interests_json is not None else []
        self.address = AddressDTO(member.address)
