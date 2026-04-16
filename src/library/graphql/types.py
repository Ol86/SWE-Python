"""Schemas for GraphQL types."""

from datetime import date

import strawberry

from library.entity.gender import Gender
from library.entity.genre import Genre


@strawberry.input
class AddressInput:
    """Address input for GraphQL."""

    postal_code: str
    """The postal code"""

    place: str
    """The place"""


@strawberry.input
class BookInput:
    """Book input for GraphQL."""

    name: str
    """The name of the book"""

    isbn: str
    """The ISBN of the book"""

    author: str
    """The author of the book"""

    still_borrowed: bool
    """Whether the book is still borrowed"""

    genre: Genre
    """The genre of the book"""


@strawberry.input
class MemberInput:
    """Member input for GraphQL."""

    username: str
    """The username of the member"""

    first_name: str
    """The first name of the member"""

    last_name: str
    """The last name of the member"""

    gender: Gender
    """The gender of the member"""

    date_of_birth: date
    """The date of birth of the member"""

    member_since: date
    """Since when the person is a member in the library."""

    is_student: bool
    """Member's student status due to discount"""

    interests: list[Genre]
    """The interests of the member"""

    email_address: str
    """The email address of the member"""

    address: AddressInput
    """The address of the member"""

    books: list[BookInput]
    """The books currently and previously borrowed by the member"""


@strawberry.type
class CreatePayload:
    """Payload for creating a member."""

    id: int
    """The generated ID of the created member."""


@strawberry.type
class LoginResult:
    """Result of a login attempt."""

    token: str
    """The generated token for the logged in member."""

    expires: str
    """The expiration time of the generated token."""

    roles: list[str]
    """The roles of the logged in member."""
