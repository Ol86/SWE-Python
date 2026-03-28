"""
The REST API router for member read operations,
such as retrieving member information, listing members, and searching for members.
"""

from typing import Final

from fastapi import APIRouter

__all__ = [
    "member_router",
]

member_router: Final = APIRouter(tags=["Read"])
