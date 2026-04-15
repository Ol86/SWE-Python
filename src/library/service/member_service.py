"""The bussiness logic for member read operations."""

from collections.abc import Mapping
from typing import Final

from loguru import logger

from library.repository import MemberRepository, Pageable, Session, Slice
from library.security import Role, User
from library.service.exceptions import ForbiddenError, NotFoundError
from library.service.member_dto import MemberDTO

__all__ = [
    "MemberService",
]


class MemberService:
    """The service class for member read operations."""

    def __init__(self, repo: MemberRepository) -> None:
        """Initialize the MemberService with a MemberRepository instance."""
        self.repo: MemberRepository = repo

    def find_by_id(self, member_id: int, user: User) -> MemberDTO:
        """Find a member by their ID and return a MemberDTO.

        :param member_id: The ID of the member to find.
        :param user: The user making the request.
        :return: A MemberDTO representing the member with the given ID, or None if not found.
        :rtype: MemberDTO | None
        """
        logger.debug("member_id={}", member_id)

        with Session() as session:
            user_is_admin: bool = Role.ADMIN in user.roles

            if (member := self.repo.find_by_id(member_id=member_id, session=session)) is None:
                if user_is_admin:
                    message = f"Member with id {member_id} not found."
                    logger.debug("NotFoundError", message)
                    raise NotFoundError(member_id=member_id)
                logger.debug("Not a admin user.")
                raise ForbiddenError

            if member.username != user.username and not user_is_admin:
                logger.debug("member.username={}, user.username={}, user.roles={}", member.username, user.username, user.roles)
                raise ForbiddenError

            member_dto: Final = MemberDTO(member)
            session.commit()

        logger.debug("member_dto={}", member_dto)
        return member_dto

    def find(self, searchparams: Mapping[str, str], pageable: Pageable) -> Slice[MemberDTO]:
        """Find members based on search parameters and pagination, and return a Slice of MemberDTOs.

        :param searchparams: A mapping of search parameters to filter members.
        :param pageable: The pagination information for the query.
        :return: A slice of MemberDTOs matching the search parameters and pagination.
        :rtype: Slice[MemberDTO]
        """
        logger.debug(f"{searchparams}")
        with Session() as session:
            member_slice: Final = self.repo.find(searchparams=searchparams, pageable=pageable, session=session)
            if len(member_slice.content) == 0:
                raise NotFoundError(searchparam=searchparams)

            member_dto: Final = tuple(MemberDTO(member) for member in member_slice.content)
            session.commit()

        member_dto_slice: Final = Slice(content=member_dto, total_elements=member_slice.total_elements)
        logger.debug("member_dto_slice={}", member_dto_slice)
        return member_dto_slice
