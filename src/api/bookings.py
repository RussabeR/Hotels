from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    NoAvailableRoomsException,
    NoAvailableRoomsHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    ObjectNotFoundException,
)
from src.schemas.bookings_schema import BookingAddRequest, BookingAdd
from src.schemas.hotels_schema import Hotel
from src.schemas.rooms_schema import Room
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()


@router.get("/me")
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_user_bookings(user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except NoAvailableRoomsException:
        raise NoAvailableRoomsHTTPException
    return booking


@router.delete("")
async def delete_user_bookings(db: DBDep, user_id: UserIdDep):
    await db.bookings.delete_filtered(user_id=user_id)
    await db.commit()
    return {"Ok"}
