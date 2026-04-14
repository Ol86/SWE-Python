"""Tests for Mutation with GraphQL."""

from http import HTTPStatus
from typing import Final

from constants import CTX, GRAPHQL_URL
from httpx import post
from pytest import mark


@mark.graphql
@mark.mutation
def test_create_member() -> None:
    """Test for creating a new member using GraphQL API."""
    #arrange
    query: Final = {
        "query": """
            mutation {
                create_member(
                    memberInput: {
                        username: "test_member_graphql"
                        first_name: "Mutation"
                        last_name: "Test"
                        gender: MALE
                        date_of_birth: "1990-01-01"
                        member_since: "2020-01-01"
                        is_student: false
                        email_address: "mutationmember@graphql.com"
                        interests: [FANTASY]
                        address: {
                            postal_code: "12345"
                            place: "Test City"
                            }
                        books: [
                            {
                                name: "GraphQL Testing"
                                isbn: "978-3-16-148410-0"
                                author: "John Doe"
                                still_borrowed: true
                                genre: FANTASY
                            }
                        ]
                    }
                ) {
                    id
                }
            }

            """,
    }
    #act
    response: Final = post(GRAPHQL_URL, json=query, verify=CTX)

    #assert
    assert response is not None
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert isinstance(response_body["data"]["create"]["id"], int)
    assert response_body.get("errors") is None
