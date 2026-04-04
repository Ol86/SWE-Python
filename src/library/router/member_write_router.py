"""The REST API router for member write operations."""
from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger
from patient.router.dependencies import get_write_service

from library.router.dependencies import get_member_write_service
from library.router.member_creation_model import MemberCreationModel
from library.service import MemberWriteService

__all__ = [
    "member_write_router",
]

member_write_router: Final = APIRouter(tags=["Write"])


@member_write_router.post("")
def post(
    member_model: MemberCreationModel,
    request: Request,
    service: Annotated[MemberWriteService, Depends(get_write_service)]
) -> Response:
    """Create new member.

    :param member_model: New member data.
    :param request: Request object.
    :param service: Write service object
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
