"""Fixtures for REST API tests."""

from common_test import check_readiness, db_populate, keycloak_populate
from pytest import fixture

session_scope = "session"


@fixture(scope=session_scope, autouse=True)
def check_readiness_per_session():
    """Check the readiness of the application before running tests."""
    check_readiness()
    print("Application is ready for testing.")


@fixture(scope=session_scope, autouse=True)
def populate_per_session():
    """Fixture for populating the database."""
    db_populate()
    print("Database populated for testing.")
    keycloak_populate()
    print("Keycloak populated for testing.")
