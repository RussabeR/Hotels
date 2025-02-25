from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class RoomsORrm(Base):
    __tablename__ = 'Rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('Hotels.id'))
    title: Mapped[str] = mapped_column(String(100))
    cost: Mapped[int]
    quantity: Mapped[int]
    description: Mapped[str] = mapped_column(String(100), nullable=True)
