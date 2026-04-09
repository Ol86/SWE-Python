"""The Gender enum."""

from enum import StrEnum

import strawberry


@strawberry.enum
class Gender(StrEnum):
    """Enum for gender."""

    MALE = "M"

    FEMALE = "F"

    DIVERSE = "D"
