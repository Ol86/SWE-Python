"""The Repository for managing member entities."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from library.entity.member import Member
from library.repository.pageable import Pageable
from library.repository.slice import Slice

__all__ = ["MemberRepository"]


class MemberRepository:
    """Repository for managing member entities."""

    # ------------------------------------------------------------------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------------------------------------------------------------------
    def find_by_id(self, member_id: int | None, session: Session) -> Member | None:
        """Find a member by their ID.

        :param member_id: The ID of the member to find.
        :param session: The database session to use for the query.
        :return: The member with the given ID, or None if not found.
        :rtype: Member | None
        """
        logger.debug("member_id={}", member_id)

        if member_id is None:
            return None

        statement: Final = select(Member).options(joinedload(Member.address)).where(Member.id == member_id)
        member: Final = session.scalar(statement)

        logger.debug("member={}", member)
        return member

    def find(self, searchparams: Mapping[str, str], pageable: Pageable, session: Session) -> Slice[Member]:
        """Find members based on search parameters and pagination.

        :param searchparams: A mapping of search parameters to filter members.
        :param pageable: The pagination information for the query.
        :param session: The database session to use for the query.
        :return: A slice of members matching the search parameters and pagination.
        :rtype: Slice[Member]
        """
        logger.debug(f"{searchparams}")

        if not searchparams:
            return self._find_all(pageable=pageable, session=session)

        for key, value in searchparams.items():
            if key == "username":
                member = self._find_by_username(username=value, session=session)
                logger.debug(f"{member}")
                return Slice(content=(member,), total_elements=1) if member is not None else Slice(content=(), total_elements=0)
            if key == "last_name":
                member = self._find_by_last_name(username=value, session=session)
                logger.debug(f"{member}")
                return Slice(content=(member,), total_elements=1) if member is not None else Slice(content=(), total_elements=0)
            if key == "email_address":
                member = self._find_by_email_address(username=value, session=session)
                logger.debug(f"{member}")
                return Slice(content=(member,), total_elements=1) if member is not None else Slice(content=(), total_elements=0)
        return Slice(content=(), total_elements=0)

    def _find_all(self, pageable: Pageable, session: Session) -> Sequence[Member]:
        """Find all members in the database.

        :param pageable: The pagination information for the query.
        :param session: The database session to use for the query.
        :return: A sequence of all members in the database.
        :rtype: Sequence[Member]
        """
        logger.debug("_find_all")
        offset = pageable.page_number * pageable.page_size
        statement: Final = (
            select(Member).options(joinedload(Member.address)).offset(offset).limit(pageable.page_size)
            if pageable.page_size != 0
            else select(Member).options(joinedload(Member.address))
        )
        members: Final = (session.scalars(statement)).all()
        count: Final = self._count_all_rows(session)
        member_slice: Final = Slice(content=tuple(members), total_elements=count)
        logger.debug("member_slice={}", member_slice)
        return member_slice

    def _count_all_rows(self, session: Session) -> int:
        """Count the total number of rows of the Member table.

        :param session: The database session to use
        :return: The total number of rows in the Member table.
        :rtype: int
        """
        statement: Final = select(func.count()).select_from(Member)
        count: Final = session.execute(statement).scalar()
        logger.debug("count={}", count)
        return count if count is not None else 0

    def _find_by_username(self, username: str, session: Session) -> Member | None:
        """Find a member by their username.

        :param username: The username of the member to find.
        :param session: The database session to use for the query.
        :return: The member with the given username, or None if not found.
        :rtype: Member | None
        """
        logger.debug("username={}", username)
        statement: Final = select(Member).options(joinedload(Member.address)).where(Member.username == username)
        member: Final = session.scalar(statement)
        logger.debug("member={}", member)
        return member

    def _find_by_last_name(self, last_name: str, session: Session) -> Member | None:
        """Find a member by their last name.

        :param last_name: The last name of the member to find.
        :param session: The database session to use for the query.
        :return: The member with the given last name, or None if not found.
        :rtype: Member | None
        """
        logger.debug("last_name={}", last_name)
        statement: Final = select(Member).options(joinedload(Member.address)).where(Member.last_name == last_name)
        member: Final = session.scalar(statement)
        logger.debug("member={}", member)
        return member

    def _find_by_email_address(self, email_address: str, session: Session) -> Member | None:
        """Find a member by their email address.

        :param email_address: The email address of the member to find.
        :param session: The database session to use for the query.
        :return: The member with the given email address, or None if not found.
        :rtype: Member | None
        """
        logger.debug("email_address={}", email_address)
        statement: Final = select(Member).options(joinedload(Member.address)).where(Member.email == email_address)
        member: Final = session.scalar(statement)
        logger.debug("member={}", member)
        return member

    # ------------------------------------------------------------------------------------------------------------------------------
    # Create operations
    # ------------------------------------------------------------------------------------------------------------------------------
