from fastapi import Query, APIRouter, Body
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms_schema import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение списка номеров отеля")
async def get_room(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить информацию по номеру")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_non(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms",
             summary="Добавление номера")
async def create_room(hotel_id: int,
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
    async with async_session_maker() as session:
        await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Полное изменение номера",
            description="<h1>Тут мы полностью обновляем данные о номере</h1>")
async def edit_room(hotel_id: int,
                    room_id: int,
                    room_data: RoomAddRequest
                    ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление выбранного номера")
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="<h1>Тут мы частично обновляем данные о номере</h1>",
)
async def partially_edit_room(hotel_id: int,
                              room_id: int,
                              room_data: RoomPatchRequest
                              ):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        await session.commit()
        return {"status": "OK"}
