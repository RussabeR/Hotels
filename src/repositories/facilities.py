from sqlalchemy import select, delete, insert
from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomFacilitiesOrm
from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities_schema import RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesOrm
    schema = RoomFacility

    async def set_room_facilities(self, room_id: int, facility_id: list[int]) -> None:
        get_current_facilities_ids_query = select(self.model.facility_id).filter_by(
            room_id=room_id
        )
        result = await self.session.execute(get_current_facilities_ids_query)
        current_facility_ids: list[int] = result.scalars().all()

        id_to_delete: list = list(set(current_facility_ids) - set(facility_id))
        id_to_insert: list = list(set(facility_id) - set(current_facility_ids))

        if id_to_delete:
            delete_m2m_facilities_stmt = delete(self.model).filter(
                self.model.room_id == room_id, self.model.facility_id.in_(id_to_delete)
            )
            await self.session.execute(delete_m2m_facilities_stmt)
        if id_to_insert:
            insert_m2m_facilities_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in id_to_insert]
            )
            await self.session.execute(insert_m2m_facilities_stmt)
