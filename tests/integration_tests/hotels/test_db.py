from src.schemas.hotels_schema import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="New age", location="Moscow")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
