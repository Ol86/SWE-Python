"""The module contains the FastAPI application instance for the SWE API project.

The `app` variable is an instance of `FastAPI` that can be used to define API routes and handlers.
"""

from contextlib import asynccontextmanager
from time import time
from typing import TYPE_CHECKING, Any, Final

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.gzip import GZipMiddleware
from library.problem_details import create_problem_details
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from library.banner import banner
from library.config.dev.db_populate import db_populate
from library.config.dev.db_populate_router import router as db_populate_router
from library.config.dev.keycloak_populate import keycloak_populate
from library.config.dev.keycloak_populate_router import router as keycloak_populate_router
from library.config.dev_mode import dev_db_populate, dev_keycloak_populate
from library.repository.session_factory import engine
from library.router import member_router, member_write_router, shutdown_router
from library.security import router as auth_router
from library.security import AuthorizationError, LoginError, set_response_headers
from library.service import (
    EmailExistsError,
    ForbiddenError,
    NotFoundError,
    UsernameExistsError,
    VersionOutdatedError,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Awaitable, Callable


TEXT_PLAIN: Final = "text/plain"


# ----------------------------------------------------------------------------------------------------------------------------------
# Startup and Shutdown
# ----------------------------------------------------------------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Lifespan function to handle startup and shutdown events."""
    if dev_db_populate:
        db_populate()
    if dev_keycloak_populate:
        keycloak_populate()
    banner(app.routes)
    yield
    logger.info("Shutting down the FastAPI application.")
    logger.info("Connection-Pool for the DB closed.")
    engine.dispose()


app: Final = FastAPI(lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

app.add_middleware(GZipMiddleware, minimum_size=500)


@app.middleware("http")
async def log_request_header(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Middleware to log the request headers."""
    logger.debug(f"{request.method} '{request.url}'")
    return await call_next(request)


@app.middleware("http")
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
app.include_router(auth_router, prefix="/auth")
app.include_router(shutdown_router, prefix="/admin")

if dev_db_populate:
    app.include_router(db_populate_router, prefix="/dev")
if dev_keycloak_populate:
    app.include_router(keycloak_populate_router, prefix="/dev")


@app.get("/")
def hello_world() -> dict:
    """Return a simple hello world message."""
    return {"message": "Hello, World!"}


# ----------------------------------------------------------------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------------------------------------------------------------
@app.middleware("http")
async def add_security_headers(request: Request, call_next: Callable[[Any], Awaitable[Response]]) -> Response:
    """Middleware to add security headers to the response."""
    response: Final[Response] = await call_next(request)
    set_response_headers(response)
    return response

# ----------------------------------------------------------------------------------------------------------------------------------
# Exception Handling
# ----------------------------------------------------------------------------------------------------------------------------------
@app.add_exception_handler(NotFoundError)
def not_found_exception_handler(_request: Request, _err: NotFoundError) -> Response:
    """Exception handler for NotFoundError.

    :param _request: The incoming request that caused the exception.
    :param _err: The NotFoundError exception that was raised.
    :return: A Response object with a 404 status code and the error message as plain.
    """
    return create_problem_details(status_code=status.HTTP_404_NOT_FOUND)


@app.add_exception_handler(ForbiddenError)
def forbidden_exception_handler(_request: Request, _err: ForbiddenError) -> Response:
    """Exception handler for ForbiddenError.

    :param _request: The incoming request that caused the exception.
    :param _err: The ForbiddenError exception that was raised.
    :return: A Response object with a 403 status code and the error message as plain.
    """
    return create_problem_details(status_code=status.HTTP_403_FORBIDDEN)


@app.add_exception_handler(AuthorizationError)
def authorization_exception_handler(_request: Request, _err: AuthorizationError) -> Response:
    """Exception handler for AuthorizationError.

    :param _request: The incoming request that caused the exception.
    :param _err: The AuthorizationError exception that was raised.
    :return: A Response object with a 401 status code and the error message as plain.
    """
    return create_problem_details(status_code=status.HTTP_401_UNAUTHORIZED)


@app.add_exception_handler(LoginError)
def login_exception_handler(_request: Request, _err: LoginError) -> Response:
    """Exception handler for LoginError.

    :param _request: The incoming request that caused the exception.
    :param _err: The LoginError exception that was raised.
    :return: A Response object with a 401 status code and the error message as plain.
    """
    return create_problem_details(status_code=status.HTTP_401_UNAUTHORIZED)


@app.add_exception_handler(EmailExistsError)
def email_exists_exception_handler(_request: Request, err: EmailExistsError) -> Response:
    """Exception handler for EmailExistsError.

    :param _request: The incoming request that caused the exception.
    :param err: The EmailExistsError exception that was raised.
    :return: A Response object with a 409 status code and the error message as plain.
    """
    return create_problem_details(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(err),
    )


@app.add_exception_handler(UsernameExistsError)
def username_exists_exception_handler(_request: Request, err: UsernameExistsError) -> Response:
    """Exception handler for UsernameExistsError.

    :param _request: The incoming request that caused the exception.
    :param err: The UsernameExistsError exception that was raised.
    :return: A Response object with a 409 status code and the error message as plain.
    """
    return create_problem_details(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(err),
    )
