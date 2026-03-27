"""
This module contains the ASGI server for the SWE API.
It uses Uvicorn to run the FastAPI application defined in `project.fastapi_app`.
The `run` function starts the server on localhost at port 8000 using the h11 HTTP protocol.
"""

from ssl import PROTOCOL_TLS_SERVER

import uvicorn

from library.config import (
    host_binding,
    port,
    tls_certfile,
    tls_keyfile,
)
from library.fastapi_app import app  # noqa: F401

__all__: list[str] = ["run"]


def run() -> None:
    """
    Run the ASGI server.
    """
    uvicorn.run(
        "library:app",
        http="h11",
        interface="asgi3",
        host=host_binding,
        port=port,
        ssl_certfile=tls_certfile,
        ssl_keyfile=tls_keyfile,
        ssl_version=PROTOCOL_TLS_SERVER,
    )
