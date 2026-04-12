"""Module for GraphQL API."""

from library.graphql.schema import Mutation, Query, graphql_router
from library.graphql.types import (
    AddressInput,
    BookInput,
    CreatePayload,
    MemberInput,
)

__all__ = [
    "AddressInput",
    "BookInput",
    "CreatePayload",
    "MemberInput",
    "Mutation",
    "Query",
    "graphql_router",
]
