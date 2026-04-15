"""Tests for PUT requests to the REST API."""

from http import HTTPStatus
from typing import Final

from common_test import login
from constants import CTX, REST_URL
from httpx import put
from pytest import mark


@mark.rest
@mark.put_request
def test_update_member() -> None:
    """Test for updating an existing member using REST API."""
    # arrange
    token: Final = login()
    assert token is not None
    member_id: Final = 3
    if_match: Final = '"0"'
    updated_member_data: Final = {
        "username": "updated_member_rest",
        "first_name": "Rest",
        "last_name": "Updated",
        "gender": "M",
        "date_of_birth": "1990-01-01",
        "member_since": "2020-01-01",
        "is_student": False,
        "email_address": "updated_member@example.com",
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{REST_URL}/{member_id}",
        json=updated_member_data,
        headers=headers,
        verify=CTX,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.text
