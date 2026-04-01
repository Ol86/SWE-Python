"""The bussiness logic for member read operations."""

from library.repository.member_repository import MemberRepository

__all__ = [
    "MemberService",
]


class MemberService:
    """The service class for member read operations."""

    def __init__(self, repo: MemberRepository) -> None:
        """Initialize the MemberService with a MemberRepository instance."""
        self.repo: MemberRepository = repo
