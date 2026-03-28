"""Entity class for an address"""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from library.entity.base import Base
from library.entity.member import Member


class Address(Base):
    """Entity class for an address"""

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(Identity(start=1000), primary_key=True)
    """The ID, starting at 1000"""

    postal_code: Mapped[str]
    """Postal Code"""

    place: Mapped[str]
    """Place of the member"""

    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    """The ID of the member that lives at the address as a Foreign Key"""

    member: Mapped[Member] = relationship(back_populates="address")
    """Transient Member object"""

    def __repr__(self) -> str:
        """Address data without member data"""
        return (
            f"Address(id={self.id}, postal_code={self.postal_code}, place={self.place})"
        )
