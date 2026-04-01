"""The bussiness logic for member write operations."""

from loguru import logger

from library.repository.member_repository import MemberRepository
from library.repository.session_factory import Session
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

    def delete_by_id(self, member_id: int) -> None:
        """Delete a member by their ID.

        :param member_id: The ID of the member to delete.
        """
        logger.debug("member_id={}", member_id)
        with Session() as session:
            self.repo.delete_by_id(member_id=member_id, session=session)
            session.commit()
