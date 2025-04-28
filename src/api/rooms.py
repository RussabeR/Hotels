from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep
from src.exceptions import (
    RoomNotFoundException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
    handle_room_and_hotel_exceptions,
)
from src.schemas.rooms_schema import (
    RoomAddRequest,
    RoomPatchRequest,
)
from src.exceptions import RoomNotFoundHTTPException
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение списка номеров отеля")
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples="2025-03-04"),
    date_to: date = Query(examples="2025-03-15"),
):
    return await RoomService(db).get_filtered_by_tyme(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить информацию по номеру")
@cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(room_id, hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Добавление номера")
@handle_room_and_hotel_exceptions
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    room = await RoomService(db).create_room(hotel_id, room_data)
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное изменение номера",
    description="<h1>Тут мы полностью обновляем данные о номере</h1>",
)
@handle_room_and_hotel_exceptions
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление выбранного номера")
@handle_room_and_hotel_exceptions
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException()
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="<h1>Тут мы частично обновляем данные о номере</h1>",
)
@handle_room_and_hotel_exceptions
async def partially_edit_room(
    hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep
):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}
