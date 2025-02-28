from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORrm
from src.schemas.bookings_schema import Booking


class BookingsRepository(BaseRepository):
    model = RoomsORrm
    schema = Booking
