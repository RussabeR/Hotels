from src.schemas.facilities_schema import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import sleep_task


class FacilityService(BaseService):
    async def create_facility(self, data: FacilityAdd):
        await self.db.facilities.add(data)
        await self.db.commit()

        sleep_task.delay()
