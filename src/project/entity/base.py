"""Base class for entity classes"""

from typing import TYPE_CHECKING, Any

from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    class MappedAsDataclass:

        def __init__(self, *arg: Any, **kw: Any) -> None:
            pass
else:
    from sqlalchemy.orm import MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for entity classes as dataclass"""
    pass