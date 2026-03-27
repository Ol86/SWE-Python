"""
This module serves as the entry point for the SWE API project.
It imports the `run` function from the `asgi_server` module and executes it when the module is run as a script.
The `run` function is responsible for starting the ASGI server that hosts the FastAPI application
defined in the `fastapi_app` module.
"""

from library.asgi_server import run

__all__: list[str] = ["run"]

if __name__ == "__main__":
    run()
