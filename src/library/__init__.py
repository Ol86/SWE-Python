"""The module contains the main entry points for the SWE API project."""

from library.asgi_server import run
from library.fastapi_app import app

__all__: list[str] = ["app", "run"]


def main() -> None:
    """Start the main entry point for the SWE API project."""
    run()
