"""The package provides the REST API routes for the project."""

from collections.abc import Sequence

from library.router.member_router import member_router
from library.router.member_write_router import member_write_router

__all__: Sequence[str] = [
    "member_router",
    "member_write_router",
]
