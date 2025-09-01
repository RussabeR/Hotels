import typing
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

if typing.TYPE_CHECKING:
    from src.models.facilities import FacilitiesOrm


class RoomsORrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]
    quantity: Mapped[int]
    description: Mapped[str] = mapped_column(String(100), nullable=True)

    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        back_populates="rooms", secondary="rooms_facilities"
    )
