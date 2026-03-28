"""The REST API router for member read operations."""

from typing import Final

from fastapi import APIRouter

__all__ = [
    "member_router",
]

member_router: Final = APIRouter(tags=["Read"])
