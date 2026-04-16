"""Locustfile for load testing the library API."""

from typing import Final, Literal

import urllib3
from locust import HttpUser, constant_throughput, task

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GetUser(HttpUser):
    """Locust user for load testing the library API."""

    wait_time = constant_throughput(0.1)
    MIN_USERS: Final = 100
    MAX_USERS: Final = 100

    def on_start(self) -> None:
        """Set up the user by logging in."""
        self.client.verify = False

        response: Final = self.client.post(url="/auth/token", json={"username": "admin", "password": "p"})
        body: Final[dict[Literal["token"], str]] = response.json()
        token: Final = body["token"]
        self.client.headers = {"Authorization": f"Bearer {token}"}

    @task(50)
    def get_id(self) -> None:
        """Get a user by ID."""
        for member_id in [1, 2, 3]:
            response = self.client.get(url=f"/rest/{member_id}")
            print(f"{response.json()['id']}")

    @task(50)
    def get_username(self) -> None:
        """Get a user by username."""
        for username in [
            "admin",
            "ole",
            "paul",
        ]:
            self.client.get(url="/rest", params={"username": username})

    @task(50)
    def get_email(self) -> None:
        """Get a user by email."""
        for email in [
            "admin@example.com",
            "ole.menke@example.com",
            "paul.braeuninger@example.com",
        ]:
            self.client.get(url="/rest", params={"email_address": email})
