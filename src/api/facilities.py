from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities_schema import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get('')
async def get_all_facilities(
        db: DBDep,
):
    return await db.facilities.get_all()


@router.post('')
async def create_facility(
        db: DBDep,
        facility_data: FacilityAdd
):
    facilities = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facilities}
