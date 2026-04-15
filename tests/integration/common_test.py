"""General data for integration tests."""

from http import HTTPStatus
from typing import Any, Final

from constants import (
    BASE_URL,
    CTX,
    DB_POPULATE_PATH,
    GRAPHQL_PATH,
    HEALTH_URL,
    KEYCLOAK_POPULATE_PATH,
    PASSWORD_ADMIN,
    TIMEOUT,
    TOKEN_PATH,
    USERNAME_ADMIN,
)
from httpx import get, post

__all__ = [
    "db_populate",
    "keycloak_populate",
    "login",
    "login_graphql",
]


def check_readiness() -> None:
    response: Final = get(f"{HEALTH_URL}/readiness", verify=CTX)
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"readiness mit Statuscode {response.status_code}")

    response_body: Final = response.json()
    if not isinstance(response_body, dict):
        raise RuntimeError("readiness ohne Dictionary im Response-Body")

    status: Final[Any | None] = response_body.get("db")
    if status != "up":
        raise RuntimeError(f"readiness mit Meldungstext {status}")


def login(  # noqa: D103
    username: str = USERNAME_ADMIN,
    password: str = PASSWORD_ADMIN,  # NOSONAR
) -> str:
    login_data: Final = {"username": username, "password": password}

    response: Final = post(
        f"{BASE_URL}{TOKEN_PATH}",
        json=login_data,
        verify=CTX,
        timeout=TIMEOUT,
    )
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"login() mit Statuscode {response.status_code}")

    response_body: Final = response.json()
    token: Final = response_body.get("token")

    if token is None or not isinstance(token, str):
        raise RuntimeError(f"login() mit ungueltigem Token: type={type(token)}")

    return token


def login_graphql(  # noqa: D103
    username: str = USERNAME_ADMIN,
    password: str = PASSWORD_ADMIN,  # NOSONAR
) -> str:
    login_query: Final = {"query": (f'mutation {{ login(username: "{username}", password: "{password}") {{ token }} }}')}

    response: Final = post(
        f"{BASE_URL}{GRAPHQL_PATH}",
        json=login_query,
        verify=CTX,
        timeout=TIMEOUT,
    )
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"login() mit Statuscode {response.status_code}")

    response_body: Final = response.json()
    token: Final = response_body.get("data", {}).get("login", {}).get("token")

    if token is None or not isinstance(token, str):
        raise RuntimeError(f"login_graphql() mit ungueltigem Token: type={type(token)}")

    return token


def db_populate() -> None:  # noqa: D103
    token: Final = login()
    headers: Final = {"Authorization": f"Bearer {token}"}

    response: Final = post(
        f"{BASE_URL}{DB_POPULATE_PATH}",
        headers=headers,
        verify=CTX,
    )

    assert response.status_code == HTTPStatus.OK


def keycloak_populate() -> None:  # noqa: D103
    token: Final = login()
    headers: Final = {"Authorization": f"Bearer {token}"}

    response: Final = post(
        f"{BASE_URL}{KEYCLOAK_POPULATE_PATH}",
        headers=headers,
        verify=CTX,
    )

    assert response.status_code == HTTPStatus.OK
