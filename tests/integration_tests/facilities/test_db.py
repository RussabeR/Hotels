from src.schemas.facilities_schema import FacilityAdd


async def test_db_facilities(db):
    facility_data = FacilityAdd(title="Sauna")
    new_facility_data = await db.facilities.add(facility_data)
    await db.commit()
