from datetime import date

from src.exceptions import (
    check_dates_from_dates_to,
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.hotels_schema import HotelAdd, HotelPATCH, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ):
        check_dates_from_dates_to(date_to, date_from)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, data: HotelAdd):
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def partially_edit_hotel(
        self, hotel_id: int, data: HotelPATCH, exclude_unset: bool = False
    ):
        await self.db.hotels.edit(data, exclude_unset=exclude_unset, id=hotel_id)
        await self.db.commit()

    async def check_hotel_exist(self, hotel_id: int) -> Hotel:
        try:
            room = await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundHTTPException
        return room
