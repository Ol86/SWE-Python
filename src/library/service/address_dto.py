"""Data Transfer Object for address data."""

from dataclasses import dataclass

from library.entity import Address


@dataclass(eq=False, slots=True, kw_only=True)
# TODO Strawberry
class AddressDTO:
    """DTO class for address information."""

    postal_code: str
    place: str

    def __init__(self, address: Address):
        """Initialize AddressDTO by using Address object.

        :param address: Address object
        """
        self.postal_code = address.postal_code
        self.place = address.place
