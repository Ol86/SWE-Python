from library.asgi_server import run
from library.fastapi_app import app

__all__: list[str] = ["run", "app"]


def main() -> None:
    run()
