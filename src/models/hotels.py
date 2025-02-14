from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class HotelsORrm(Base):
    __tablename__ = 'Hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
