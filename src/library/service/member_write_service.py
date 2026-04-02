"""The bussiness logic for member write operations."""

from typing import Final

from loguru import logger

from library.entity.member import Member
from library.repository.member_repository import MemberRepository
from library.repository.session_factory import Session
from library.security.user_service import UserService
from library.service.exceptions import EmailExistsError, NotFoundError, VersionOutdatedError
from library.service.member_dto import MemberDTO

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

    def update(self, member: Member, member_id: int, version: int) -> MemberDTO:
        """Update data of a current member.

        :param member: New member data
        :param member_id: ID of member to update
        :param version: Version number
        :return: Updated member
        :rtype: MemberDTO
        :raises NotFoundError: If member doesn't exist.
        :raises VersionOutdatedError: If verson isn't up to date.
        :raises EmailExistsError: If email address is already existing.
        """
        logger.debug("member_id={}, version={}, member={}", member_id, version, member)

        with Session() as session:
            member_db = self.repo.find_by_id(member_id=member_id, session=session)

            if member_db is None:
                raise NotFoundError(member_id)
            if member_db.version > version:
                raise VersionOutdatedError(version)

            email_address: Final = member.email_address
            if email_address != member_db.email and self.repo.exists_email_already(
                member_id=member_id,
                email_address=email_address,
                session=session
            ):
                raise EmailExistsError(email_address)

            member_db.set(member)

            member_updated = self.repo.update(member=member_db, session=session)

            if member_updated is None:
                raise NotFoundError(member_id)
            member_dto: Final = MemberDTO(member_updated)
            logger.debug("{}", member_dto)

            session.commit()
            member_dto.version += 1

            return member_dto

    def delete_by_id(self, member_id: int) -> None:
        """Delete a member by their ID.

        :param member_id: The ID of the member to delete.
        """
        logger.debug("member_id={}", member_id)
        with Session() as session:
            self.repo.delete_by_id(member_id=member_id, session=session)
            session.commit()
