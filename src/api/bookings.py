from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings_schema import BookingAddRequest, BookingAdd, Booking

router = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.get("")
async def get_all_bookings(
        db: DBDep
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_user_bookings(
        db: DBDep,
        user_id: UserIdDep
):
    return await db.bookings.get_filtered(user_id=user_id)


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
    print(_booking_data)
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.delete("")
async def delete_user_bookings(
        db: DBDep,
        user_id: UserIdDep
):
    await db.bookings.delete_filtered(user_id=user_id)
    await db.commit()
    return {'Ok'}
