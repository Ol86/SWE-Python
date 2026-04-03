"""The REST API router for member write operations."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Response, status
from loguru import logger

from library.router.dependencies import get_member_write_service
from library.service import MemberWriteService

__all__ = [
    "member_write_router",
]

member_write_router: Final = APIRouter(tags=["Write"])


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
