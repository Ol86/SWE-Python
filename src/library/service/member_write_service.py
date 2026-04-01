"""The bussiness logic for member write operations."""

from library.repository.member_repository import MemberRepository
from library.security.user_service import UserService

__all__ = [
    "MemberWriteService",
]


class MemberWriteService:
    """The service class for member create, update, and delete operations."""

    def __init__(self, repo: MemberRepository, user_service: UserService) -> None:
        """Initialize the MemberWriteService, with repo and user service.

        :param repo: The repository for member data access.
        :param user_service: The service for user-related operations, such as authentication and authorization.
        """
        self.repo: MemberRepository = repo
        self.user_service: UserService = user_service
