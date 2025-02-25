from fastapi import Query, APIRouter, Body

from src.api.dependencies import DBDep
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms_schema import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение списка номеров отеля")
async def get_room(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить информацию по номеру")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_non(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms",
             summary="Добавление номера")
async def create_room(hotel_id: int,
                      db: DBDep,
                      room_data: RoomAddRequest = Body(
                          openapi_examples={
                              "1": {
                                  "summary": "Сочи",
                                  "value": {
                                      "title": "2х местная, люкс",
                                      "cost": "1500",
                                      "quantity": "3",
                                      "description": "Отель находится в уютном районе города, включая прекрасные пляжи",
                                  }
                              },
                          })
                      ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.add(_room_data)
    await db.rooms.commit()
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
    await db.rooms.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление выбранного номера")
async def delete_hotel(hotel_id: int,
                       room_id: int,
                       db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.rooms.commit()
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
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
    await db.rooms.commit()
    return {"status": "OK"}
