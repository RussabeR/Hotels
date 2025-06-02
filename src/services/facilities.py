from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.schemas.facilities_schema import FacilityAdd, Facility
from src.services.base import BaseService
from src.tasks.tasks import sleep_task


class FacilityService(BaseService):
    async def create_facility(self, data: FacilityAdd):
        await self.db.facilities.add(data)
        await self.db.commit()

        sleep_task.delay()

    async def check_facility_exist(self, facility_id: int) -> Facility:
        try:
            facility = await self.db.hotels.get_one(id=facility_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        return facility
