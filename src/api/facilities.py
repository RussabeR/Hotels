from fastapi_cache.decorator import cache
from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities_schema import FacilityAdd
from src.tasks.tasks import sleep_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    print("иду в ДБ")
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd):
    facilities = await db.facilities.add(facility_data)
    await db.commit()

    sleep_task.delay()

    return {"status": "OK", "data": facilities}
