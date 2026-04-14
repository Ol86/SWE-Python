"""Pydantic model for an address."""

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, StringConstraints

from library.entity.address import Address
from library.router.constants import PLACE_PATTERN, POSTAL_CODE_PATTERN

__all__ = ["AddressModel"]


class AddressModel(BaseModel):
    """Pydantic model for an address."""

    postal_code: Annotated[str, StringConstraints(pattern=POSTAL_CODE_PATTERN)]
    """Postal Code."""

    place: Annotated[str, StringConstraints(pattern=PLACE_PATTERN, max_length=64)]
    """Place."""

    model_config = ConfigDict(json_schema_extra={"example": {"postal_code": "00000", "place": "Test"}})

    def _to_dict(self) -> dict[str, Any]:
        """Convert model into dictionary.

        :return: Book dictionary
        :rtype: dict[str, Any]
        """
        new_dict: dict = self.model_dump()
        new_dict["id"] = None
        new_dict["member_id"] = None
        new_dict["member"] = None

        return new_dict

    def to_address(self) -> Address:
        """Convert model into address object.

        :return: address object
        :rtype: Address
        """
        address_dict: dict[str, Any] = self._to_dict()

        return Address(**address_dict)
