"""The module contains the FastAPI application instance for the SWE API project.

The `app` variable is an instance of `FastAPI` that can be used to define API routes and handlers.
"""

from contextlib import asynccontextmanager
from time import time
from typing import TYPE_CHECKING, Any, Final

from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from library.config.dev.db_populate import db_populate
from library.config.dev.keycloak_populate import keycloak_populate
from library.config.dev_mode import dev_db_populate, dev_keycloak_populate
from library.repository.session_factory import engine
from library.router import member_router, member_write_router
from library.security.response_headers import set_response_headers

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Awaitable, Callable


TEXT_PLAIN: Final = "text/plain"


# ----------------------------------------------------------------------------------------------------------------------------------
# Startup and Shutdown
# ----------------------------------------------------------------------------------------------------------------------------------
@asynccontextmanager
async def lifespan() -> AsyncGenerator[None]:
    """Lifespan function to handle startup and shutdown events."""
    if dev_db_populate:
        db_populate()
    if dev_keycloak_populate:
        keycloak_populate()
    yield
    logger.info("Shutting down the FastAPI application.")
    logger.info("Connection-Pool for the DB closed.")
    engine.dispose()


app: Final = FastAPI()

Instrumentator().instrument(app).expose(app)

app.add_middleware(GZipMiddleware, minimum_size=500)


@app.middleware("http")
async def log_request_header(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Middleware to log the request headers."""
    logger.debug(f"{request.method} '{request.url}'")
    return await call_next(request)


async def log_response_time(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Middleware to log the response time."""
    start = time()
    response = await call_next(request)
    duration_ms = (time() - start) * 1000
    logger.debug(f"Response time: {duration_ms:.2f} ms, status code: {response.status_code}")
    return response


# ----------------------------------------------------------------------------------------------------------------------------------
# REST
# ----------------------------------------------------------------------------------------------------------------------------------
app.include_router(member_router, prefix="/rest")
app.include_router(member_write_router, prefix="/rest")


# ----------------------------------------------------------------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------------------------------------------------------------
@app.middleware("http")
async def add_security_headers(request: Request, call_next: Callable[[Any], Awaitable[Response]]) -> Response:
    """Middleware to add security headers to the response."""
    response: Final[Response] = await call_next(request)
    set_response_headers(response)
    return response
