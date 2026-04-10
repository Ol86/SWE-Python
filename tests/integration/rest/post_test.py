"""Tests for POST requests to the REST API."""

from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, rest_url
from httpx import post
from pytest import mark

token: str | None


@mark.rest
@mark.post_request
def test_create_member() -> None:
    """Test for creating a new member using REST API."""
    #arrange
    member_data: Final = {
        "username": "test_member_rest",
        "first_name": "REST",
        "last_name": "Test Member",
        "gender": "M",
        "date_of_birth": "1990-01-01",
        "member_since": "2020-01-01",
        "is_student": False,
        "email_address": "testmemberrest@example.com",
        "interests": ["FANTASY"],
        "address": {
            "postal_code": "12345",
            "place": "Test City",
        },
        "books": [
            {
                "name": "REST Testing",
                "isbn": "978-3-16-148410-0",
                "author": "John Doe",
                "still_borrowed": True,
                "genre": "FANTASY",
            }
        ],
    }
    headers = {"Content-Type": "application/json"}

    #act
    response: Final = post(
        rest_url,
        json=member_data,
        headers=headers,
        verify=ctx,
    )

    #assert
    assert response.status_code == HTTPStatus.CREATED
    location_header: Final = response.headers.get("Location")
    assert location_header is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location_header) is not None
    assert not response.text
