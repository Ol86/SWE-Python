from project.asgi_server import run
from project.fastapi_app import app

__all__: list[str] = ["run", "app"]


def main() -> None:
    run()
