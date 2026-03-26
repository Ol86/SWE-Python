"""Entity class for an address"""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.entity.base import Base

class Address(Base):
    """Entity class for an address"""
    
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True
    )
    """The ID, starting at 1000"""

    postal_code: Mapped[str]
    """Postal Code"""

    place: Mapped[str]
    """Place of the member"""

    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    """The ID of the member that lives at the address as a Foreign Key"""

    member: Mapped[Member] = relationship( #noqa: F821 #ty: ignore[unresolved-reference]
        back_populates="address"
    )
    """Transient Member object"""

    def __repr__(self) -> str:
        """Address data without member data"""
        return f"Address(id={self.id}, postal_code={self.postal_code}, place={self.place})"

    