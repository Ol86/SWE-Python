"""The module contains custom exceptions for the service layer."""

from collections.abc import Mapping

__all__ = ["EmailExistsError", "ForbiddenError", "NotFoundError", "UsernameExistsError", "VersionOutdatedError"]


class EmailExistsError(Exception):
    """Exception for already existing email address."""

    def __init__(self, email: str) -> None:
        """Initialize Error.

        :param email: Already existing email address
        """
        super().__init__(f"Already existing email: {email}")
        self.emal = email


class UsernameExistsError(Exception):
    """Exception for already existing username."""

    def __init__(self, username: str | None) -> None:
        """Initialize Error.

        :param username: Already existing username
        """
        super().__init__(f"Already existing username: {username}")
        self.username = username


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


class VersionOutdatedError(Exception):
    """Exception for deprecated version number during updating."""

    def __init__(self, version: int) -> None:
        """Initialize Error.

        :param version: Deprecated version number
        """
        super().__init__(f"Deprecated version: {version}")
        self.version = version
