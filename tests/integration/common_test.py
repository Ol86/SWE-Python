"""General data for integration tests."""

from http import HTTPStatus
from pathlib import Path
from ssl import create_default_context
from typing import Any, Final

from httpx import get, post

__all__ = [
    "base_url",
    "ctx",
    "db_populate",
    "db_populate_path",
    "graphql_path",
    "graphql_url",
    "health_url",
    "keycloak_populate",
    "keycloak_populate_path",
    "login",
    "login_graphql",
    "password_admin",
    "rest_path",
    "rest_url",
    "timeout",
    "token_path",
    "username_admin",
]

schema: Final = "https"
port: Final = 8000
host: Final = "127.0.0.1"
base_url: Final = f"{schema}://{host}:{port}"
rest_path: Final = "/rest"
rest_url: Final = f"{base_url}{rest_path}"
health_url: Final = f"{base_url}/health"
graphql_path: Final = "/graphql"
graphql_url: Final = f"{base_url}/graphql"
token_path: Final = "/auth/token"  # noqa: S105
db_populate_path: Final = "/dev/db_populate"
keycloak_populate_path: Final = "/dev/keycloak_populate"
username_admin: Final = "admin"
password_admin: Final = "p"  # noqa: S105  # NOSONAR
timeout: Final = 2
certificate: Final = str(Path("tests") / "integration" / "certificate.crt")
ctx = create_default_context(cafile=certificate)


def check_readiness() -> None:
    response: Final = get(f"{health_url}/readiness", verify=ctx)
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"readiness mit Statuscode {response.status_code}")
    response_body: Final = response.json()
    if not isinstance(response_body, dict):
        raise RuntimeError("readiness ohne Dictionary im Response-Body")
    status: Final[Any | None] = response_body.get("db")
    if status != "up":
        raise RuntimeError(f"readiness mit Meldungstext {status}")


def login(  # noqa: D103
    username: str = username_admin,
    password: str = password_admin,  # NOSONAR
) -> str:
    login_data: Final = {"username": username, "password": password}
    response: Final = post(
        f"{base_url}{token_path}",
        json=login_data,
        verify=ctx,
        timeout=timeout,
    )
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"login() mit Statuscode {response.status_code}")
    response_body: Final = response.json()
    token: Final = response_body.get("token")
    if token is None or not isinstance(token, str):
        raise RuntimeError(f"login() mit ungueltigem Token: type={type(token)}")
    return token


def login_graphql(  # noqa: D103
    username: str = username_admin,
    password: str = password_admin,  # NOSONAR
) -> str:
    login_query: Final = {
        "query": f'mutation {{ login(username: "{username}", password: "{password}") {{ token }} }}'  # noqa: E501
    }
    response: Final = post(
        f"{base_url}{graphql_path}",
        json=login_query,
        verify=ctx,
        timeout=timeout,
    )
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"login() mit Statuscode {response.status_code}")
    response_body: Final = response.json()
    token: Final = response_body.get("data").get("login").get("token")
    if token is None or not isinstance(token, str):
        raise RuntimeError(f"login_query() mit ungueltigem Token: type={type(token)}")
    return token


def db_populate() -> None:  # noqa: D103
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}
    response: Final = post(
        f"{base_url}{db_populate_path}",
        headers=headers,
        verify=ctx,
    )
    assert response.status_code == HTTPStatus.OK


def keycloak_populate() -> None:  # noqa: D103
    token: Final = login()
    assert token is not None
    headers: Final = {"Authorization": f"Bearer {token}"}
    response: Final = post(
        f"{base_url}{keycloak_populate_path}",
        headers=headers,
        verify=ctx,
    )
    assert response.status_code == HTTPStatus.OK
