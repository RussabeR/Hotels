from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    RoomNotFoundHTTPException,
    RoomNotFoundException,
    ObjectNotFoundException,
    NoAvailableRoomsException,
    NoAvailableRoomsException,
    NoAvailableRoomsHTTPException,
    HotelNotFoundException,
)
from src.schemas.bookings_schema import BookingAddRequest, BookingAdd
from src.schemas.hotels_schema import Hotel
from src.schemas.rooms_schema import Room
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_user_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(
        self,
        user_id: UserIdDep,
        booking_data: BookingAddRequest,
    ):
        try:
            room: Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundHTTPException
        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return {"status": "OK", "data": booking}
