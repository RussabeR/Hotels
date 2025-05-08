from datetime import date

from src.exceptions import (
    check_dates_from_dates_to,
    ObjectNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.schemas.facilities_schema import RoomFacilityAdd
from src.schemas.rooms_schema import (
    RoomAdd,
    RoomAddRequest,
    RoomPatchRequest,
    RoomPatch,
    Room,
)
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_tyme(
        self,
        hotel_id: id,
        date_from: date,
        date_to: date,
    ):
        check_dates_from_dates_to(date_to, date_from)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_to=date_to, date_from=date_from
        )

    async def get_room(self, room_id: int, hotel_id: int):
        await RoomService(self.db).check_room_exist(room_id)
        await HotelService(self.db).check_hotel_exist(hotel_id)
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(self, hotel_id: int, room_data: RoomAddRequest):
        await HotelService(self.db).check_hotel_exist(hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        await self.check_room_exist(room_id)
        await HotelService(self.db).check_hotel_exist(hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id=room_id, facility_id=room_data.facilities_ids
        )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).check_hotel_exist(hotel_id)
        await self.db.hotels.get_one(id=hotel_id)
        await self.check_room_exist(room_id)
        await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await self.db.commit()

    async def partially_edit_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
    ):
        await HotelService(self.db).check_hotel_exist(hotel_id)
        await self.check_room_exist(room_id)
        await self.db.hotels.get_one(id=hotel_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(
            _room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id
        )
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facility_id=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def check_room_exist(self, room_id: int) -> Room:
        try:
            room = await self.db.hotels.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        return room
