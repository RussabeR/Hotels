from datetime import date

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from sqlalchemy import select

from src.repositories.utils import rooms_id_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, date_from, date_to, hotel_id):
        rooms_ids_for_booking = rooms_id_for_booking(date_to=date_to, date_from=date_from, hotel_id=hotel_id)
