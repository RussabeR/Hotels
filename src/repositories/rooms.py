from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORrm
from src.schemas.rooms_schema import Room, RoomWithRels
from src.repositories.utils import rooms_id_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsORrm
    schema = Room

    async def get_filtered_by_time(self,
                                   hotel_id: int,
                                   date_from: date,
                                   date_to: date):
        rooms_ids_to_get = rooms_id_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsORrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model) for model in result.unique().scalars().all()]
