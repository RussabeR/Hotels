from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class FacilitiesOrm(Base):
    __tablename__ = 'facilities'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)


class RoomsFacilitiesOrm(Base):
    __tablename__ = 'rooms_facilities'
    id: Mapped[int] = mapped_column(primary_key=True)
    rooms_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    facilities_id: Mapped[int] = mapped_column(ForeignKey('facilities.id'))
