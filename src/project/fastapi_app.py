"""
This module contains the FastAPI application instance for the SWE API project.
The `app` variable is an instance of `FastAPI` that can be used to define API routes and handlers.
"""

from fastapi import FastAPI
from typing import Final

app: Final = FastAPI()


@app.get("/hello")
def hello_world() -> dict:
    """
    A simple API endpoint that returns a greeting message.
    """
    return dict(message="Hello, World!")
