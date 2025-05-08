from fastapi_cache.decorator import cache
from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities_schema import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    print("иду в ДБ")
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd):
    facilities = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facilities}
