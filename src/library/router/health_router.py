"""Health check routes for the SWE API."""

from typing import Any, Final

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from library.repository import engine

__all__ = ["router"]

router: Final = APIRouter(tags=["Health"])


@router.get("/liveness")
def liveness() -> dict[str, Any]:
    """Liveness check endpoint.

    :return: A dictionary indicating the status of the application.
    :rtype: dict[str, Any]
    """
    return {"status": "up"}


@router.get("/readiness")
def readiness() -> dict[str, Any]:
    """Readiness check endpoint.

    :return: A dictionary indicating the status of the database connection.
    :rtype: dict[str, Any]
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("SELECT 1"))
        except OperationalError:
            return {"db": "down"}
    return {"db": "up"}
