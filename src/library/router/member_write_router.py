"""The REST API router for member write operations."""

from typing import Final

from fastapi import APIRouter

__all__ = [
    "member_write_router",
]

member_write_router: Final = APIRouter(tags=["Write"])
