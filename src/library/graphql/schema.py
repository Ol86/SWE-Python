"""Schema for GraphQL API."""

from typing import Final

import strawberry
from fastapi import Request
from loguru import logger
from strawberry.fastapi import GraphQLRouter

from library.config.graphql import graphql_ide
from library.graphql import CreatePayload, MemberInput
from library.graphql.types import LoginResult
from library.repository import MemberRepository
from library.router.member_creation_model import MemberCreationModel
from library.security import TokenService, UserService
from library.service import MemberWriteService

_repo: Final = MemberRepository()
_user_service: UserService = UserService()
_write_service = MemberWriteService(repo=_repo, user_service=_user_service)
_token_service: Final = TokenService()


@strawberry.type
class Query:
    """Empty GraphQL query for fetching data."""

    # TODO necessary?


@strawberry.type
class Mutation:
    """GraphQL mutation for creating a member."""

    @strawberry.mutation
    def create_member(self, member_input: MemberInput) -> CreatePayload:
        """Create a new member.

        :param member_input: The input data for creating a member.
        :return: The payload containing the ID of the created member.
        :raises EmailExistsException: If the email address already exists.
        :raises UsernameExistsException: If the username already exists.
        """
        logger.debug("member_input={}", member_input)

        member_dict = member_input.__dict__
        member_dict["address"] = member_input.address.__dict__
        member_dict["books"] = [book.__dict__ for book in member_input.books]

        member_model: Final = MemberCreationModel.model_validate(member_dict)

        member_dto: Final = _write_service.create(member=member_model.to_member())
        payload: Final = CreatePayload(id=member_dto.id)

        logger.debug("payload={}", payload)
        return payload

    @strawberry.mutation
    def login(self, username: str, password: str) -> LoginResult:
        """Login a member and return a token.

        :param username: The username
        :param password: The password
        :return: The login result containing the token.
        """
        logger.debug("username={}, password={}", username, password)
        token_mapping = _token_service.token(username=username, password=password)

        token = token_mapping["access_token"]
        user = _token_service.get_user_from_token(token=token)
        roles: Final = [role.value for role in user.roles]

        return LoginResult(token=token, expires="1d", roles=roles)


schema: Final = strawberry.Schema(query=Query, mutation=Mutation)


Context = dict[str, Request]


def get_context(request: Request) -> Context:
    """Get the context for GraphQL operations.

    :param request: The incoming HTTP request.
    :return: The context containing the request.
    """
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](schema=schema, context_getter=get_context, graphql_ide=graphql_ide)
