from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings_schema import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
