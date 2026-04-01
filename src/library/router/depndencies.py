"""Factory functions for creating dependency instances."""

from typing import Annotated

from fastapi import Depends

from library.repository.member_repository import MemberRepository
from library.security.dependencies import get_user_service
from library.security.user_service import UserService
from library.service.member_service import MemberService
from library.service.member_write_service import MemberWriteService


def get_member_repository() -> MemberRepository:
    """Create a MemberRepository instance.

    :return: A new instance of MemberRepository.
    :rtype: MemberRepository
    """
    return MemberRepository()


def get_member_service(
    member_repository: Annotated[MemberRepository, Depends(get_member_repository)],
) -> MemberService:
    """Create a MemberService instance.

    :param member_repository: The MemberRepository instance to be used by the service.
    :return: A new instance of MemberService.
    :rtype: MemberService
    """
    return MemberService(member_repository)


def get_member_write_service(
    member_repository: Annotated[MemberRepository, Depends(get_member_repository)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> MemberWriteService:
    """Create a MemberWriteService instance.

    :param member_repository: The MemberRepository instance to be used by the service.
    :param user_service: The UserService instance to be used by the service.
    :return: A new instance of MemberWriteService.
    :rtype: MemberWriteService
    """
    return MemberWriteService(member_repository, user_service)
