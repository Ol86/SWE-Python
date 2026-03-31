"""The module contains custom exceptions for the service layer."""

from collections.abc import Mapping

__all__ = ["ForbiddenError", "NotFoundError"]


class ForbiddenError(Exception):
    """Exception, if the user is not authorized to access the requested resource."""


class NotFoundError(Exception):
    """Exception, if the requested resource could not be found."""

    def __init__(
        self,
        member_id: int | None = None,
        searchparam: Mapping[str, str] | None = None,
    ) -> None:
        """Initialize the NotFoundError with optional member_id and search parameters.

        :param member_id: The ID of the member that could not be found, if applicable.
        :param searchparam: The search parameters that were used to find the resource, if applicable.
        """
        super().__init__("Not Found")
        self.member_id = member_id
        self.searchparam = searchparam
