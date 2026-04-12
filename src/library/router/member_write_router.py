"""The REST API router for member write operations."""
from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from library.problem_details import create_problem_details
from library.router.constants import IF_MATCH, IF_MATCH_MIN_LEN
from library.router.dependencies import get_member_write_service
from library.router.member_creation_model import MemberCreationModel
from library.router.member_update_model import MemberUpdateModel
from library.security import Role, RolesRequired
from library.service import MemberWriteService

__all__ = [
    "member_write_router",
]

member_write_router: Final = APIRouter(tags=["Write"])


@member_write_router.post(path="")
def post(
    member_model: MemberCreationModel,
    request: Request,
    service: Annotated[MemberWriteService, Depends(get_member_write_service)]
) -> Response:
    """Create new member.

    :param member_model: New member data.
    :param request: Request object.
    :param service: Write service object
    :return: Responde with status code 201
    :rtype: Response
    :raises ValidationError: If pydantic validation fails.
    :raises EmailExistsError: If email address already exists.
    :raises UsernameExists: If username already exists.
    """
    logger.debug("member_model={}", member_model)
    member_dto: Final = service.create(member_model.to_member())
    logger.debug("member_dto={}", member_dto)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{member_dto.id}"}
    )


@member_write_router.put(
    path="/{member_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.PATIENT]))],
)
def put(
    member_id: int,
    member_update_model: MemberUpdateModel,
    request: Request,
    service: Annotated[MemberWriteService, Depends(get_member_write_service)],
) -> Response:
    """Update existing member.

    :param member_id: ID of member that is updated
    :param member_update_model: Pydantic update model with new member data
    :param request: Request object with if-match
    :param service: Write service object
    :return: Response with status code 204
    :rtype: Response
    :raises ValidationError: If validation fails
    :raises EmailExistsError: If email already exists
    :raises NotFoundError: If member_id is not found in database
    :raises VersionOutdatedError: If version number is deprecated
    """
    if_match: Final = request.headers.get(IF_MATCH)
    logger.debug(
        "member_id={}, if_match={}, member_update_model={}",
        member_id, if_match, member_update_model
    )

    if (if_match_value := _get_if_match_as_version(if_match)) is Response:
        return if_match_value
    version: Final = if_match_value # version is always int due to the line above

    member: Final = member_update_model.to_member()
    member_modified: Final = service.update(
        member=member,
        member_id=member_id,
        version=version,  # ty:ignore[invalid-argument-type]
    )
    logger.debug("member_modified={}", member_modified)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETag": f'"{member_modified.version}'}
        )


def _get_if_match_as_version(if_match) -> Response | int:
    """Check whether if-match is valid and can be converted into integer version number.

    :param if_match: If-match value
    :return: Response, if if_match is not valid, else the version
    :rtype: Response | int
    """
    if if_match is None:
        return create_problem_details(status.HTTP_428_PRECONDITION_REQUIRED)
    if (
        len(if_match) < IF_MATCH_MIN_LEN
        or not if_match.startswith('"')
        or not if_match.endswith('"')
    ):
        return create_problem_details(status.HTTP_412_PRECONDITION_FAILED)

    return _get_version_as_int(if_match)


def _get_version_as_int(if_match) -> Response | int:
    """Check whether version is valid.

    :param version: If-match value
    :rtype: Response | int
    """
    version: Final = if_match[1:-1]

    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(status_code=status.HTTP_412_PRECONDITION_FAILED)

    return version_int


@member_write_router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_member_by_id(
    member_id: int,
    service: Annotated[MemberWriteService, Depends(get_member_write_service)],
) -> Response:
    """Delete a member by their ID.

    :param member_id: The ID of the member to delete.
    :param service: The member write service.
    :return: The response indicating the result of the operation.
    :rtype: Response
    """
    logger.debug("member_id={}", member_id)
    service.delete_by_id(member_id=member_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
