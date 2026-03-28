"""
The REST API router for member write operations,
such as creating a new member, updating member information, and deleting a member.
"""

from typing import Final

from fastapi import APIRouter

__all__ = [
    "member_write_router",
]

member_write_router: Final = APIRouter(tags=["Write"])
