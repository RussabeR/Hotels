from datetime import date

from fastapi import Query, APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facilities_schema import RoomFacilityAdd
from src.schemas.rooms_schema import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение списка номеров отеля")
async def get_rooms(hotel_id: int,
                    db: DBDep,
                    date_from: date = Query(example="2025-03-04"),
                    date_to: date = Query(example="2025-03-15")
                    ):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_to=date_to, date_from=date_from)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить информацию по номеру")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms",
             summary="Добавление номера")
async def create_room(hotel_id: int,
                      db: DBDep,
                      room_data: RoomAddRequest = Body()
                      ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Полное изменение номера",
            description="<h1>Тут мы полностью обновляем данные о номере</h1>")
async def edit_room(hotel_id: int,
                    room_id: int,
                    room_data: RoomAddRequest,
                    db: DBDep
                    ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id=room_id, facility_id=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление выбранного номера")
async def delete_hotel(hotel_id: int,
                       room_id: int,
                       db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="<h1>Тут мы частично обновляем данные о номере</h1>",
)
async def partially_edit_room(hotel_id: int,
                              room_id: int,
                              room_data: RoomPatchRequest,
                              db: DBDep
                              ):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id,
                                                      facility_id=_room_data_dict["facilities_ids"])
    await db.commit()
    return {"status": "OK"}
