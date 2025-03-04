from datetime import date
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORrm
from src.schemas.rooms_schema import Room
from src.repositories.utils import rooms_id_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsORrm
    schema = Room

    async def get_filtered_by_time(self,
                                   hotel_id: int,
                                   date_from: date,
                                   date_to: date):
        rooms_ids_to_get = rooms_id_for_booking(date_from, date_to, hotel_id)

        return await self.get_filtered(RoomsORrm.id.in_(rooms_ids_to_get))
