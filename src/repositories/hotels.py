from datetime import date
from sqlalchemy import select
from src.models.rooms import RoomsORrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repositories.utils import rooms_id_for_booking
from src.schemas.hotels_schema import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_time(self,
                                   date_from: date,
                                   date_to: date
                                   ):
        rooms_ids_to_get = rooms_id_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsORrm.hotel_id)
            .select_from(RoomsORrm)
            .filter(RoomsORrm.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))
