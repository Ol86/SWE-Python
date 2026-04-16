"""The REST API router for member read operations."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from library.repository import Pageable
from library.repository.slice import Slice
from library.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from library.router.dependencies import get_member_service
from library.router.page import Page
from library.security import Role, RolesRequired, User
from library.service import MemberDTO, MemberService

__all__ = [
    "member_router",
]

member_router: Final = APIRouter(tags=["Read"])


@member_router.get(
    "/{member_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.PATIENT]))],
)
def get_member_by_id(
    member_id: int,
    request: Request,
    service: Annotated[MemberService, Depends(get_member_service)],
) -> Response:
    """Get a member by ID.

    :param member_id: The ID of the member to retrieve.
    :param request: The incoming HTTP request.
    :param service: The member service to use for retrieving the member.
    :return: A JSON response containing the member data or an error message.
    :rtype: Response
    """
    user: Final[User] = request.state.current_user
    logger.debug(f"User '{user.username}' is trying to access member with ID {member_id}.")

    member: Final = service.find_by_id(member_id, user)
    logger.debug(f"Member found: {member}")

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug(f"version={version}")
        if version is not None:
            try:
                if int(version) == member.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                logger.debug(f"Invalid version={version}")
    return JSONResponse(
        content=_member_to_dict(member),
        headers={ETAG: f'"{member.version}"'},
    )


@member_router.get(
    "",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get_member(
    request: Request,
    service: Annotated[MemberService, Depends(get_member_service)],
) -> JSONResponse:
    """Get the current member based on the authenticated user.

    :param request: The incoming HTTP request.
    :param service: The member service to use for retrieving the member.
    :return: A JSON response containing the member data or an error message.
    :rtype: JSONResponse
    """
    query_params: Final = request.query_params
    logger.debug(f"Query parameters: {query_params}")

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    searchparams = dict(query_params)
    if "page" in searchparams:
        searchparams.pop("page")
    if "size" in searchparams:
        searchparams.pop("size")

    member_slice: Final = service.find(searchparams=searchparams, pageable=pageable)

    result: Final = _member_slice_to_dict(member_slice=member_slice, pageable=pageable)
    logger.debug(f"Result: {result}")
    return JSONResponse(content=result)


def _member_slice_to_dict(
    member_slice: Slice[MemberDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    """Convert a Slice of MemberDTOs to a dictionary.

    :param member_slice: The Slice of MemberDTOs to convert.
    :param pageable: The Pageable object containing pagination information.
    :return: A dictionary representation of the Slice of MemberDTOs.
    :rtype: dict[str, Any]
    """
    member_dict: Final = tuple(_member_to_dict(member) for member in member_slice.content)
    page: Final = Page.create(
        content=member_dict,
        pageable=pageable,
        total_elements=member_slice.total_elements,
    )
    return asdict(obj=page)


def _member_to_dict(member: MemberDTO) -> dict[str, Any]:
    """Convert a MemberDTO to a dictionary.

    :param member: The MemberDTO to convert.
    :return: A dictionary representation of the MemberDTO.
    :rtype: dict[str, Any]
    """
    member_dict: Final = asdict(obj=member)
    member_dict.pop("version")
    member_dict.update({"date_of_birth": member.date_of_birth.isoformat()})
    if member.member_since is not None:
        member_dict.update({"member_since": member.member_since.isoformat()})
    return member_dict
