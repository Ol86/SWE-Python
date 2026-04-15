"""The package provides the REST API routes for the project."""

from collections.abc import Sequence

from library.router.health_router import liveness, readiness
from library.router.health_router import router as health_router
from library.router.member_router import get_member, get_member_by_id, member_router
from library.router.member_write_router import delete_member_by_id, member_write_router, post, put
from library.router.shutdown_router import router as shutdown_router
from library.router.shutdown_router import shutdown

__all__: Sequence[str] = [
    "delete_member_by_id",
    "get_member",
    "get_member_by_id",
    "health_router",
    "liveness",
    "member_router",
    "member_write_router",
    "post",
    "put",
    "readiness",
    "shutdown",
    "shutdown_router",
]
