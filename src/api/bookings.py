from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings_schema import BookingAddRequest, BookingAdd, Booking

router = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
    # insert_query = text("""
    #         INSERT INTO bookings (user_id, room_id, price, date_from, date_to)
    #         VALUES (:user_id, :room_id, :price, :date_from, :date_to)
    #         RETURNING id, user_id, room_id, price, date_from, date_to""")
    #
    # result = await db.execute(insert_query, {
    #     "user_id": _booking_data.user_id,
    #     "room_id": _booking_data.room_id,
    #     "price": _booking_data.price,
    #     "date_from": _booking_data.date_from,
    #     "date_to": _booking_data.date_to
    # })
    #
    # booking = result.mappings().first()
    #
    # await db.commit()
    #
    # return {"status": "OK", "data": booking}


@router.get("")
async def get_all_bookings(
        db: DBDep
):
    return await db.bookings.get_all()
