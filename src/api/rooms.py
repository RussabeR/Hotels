from fastapi import Query, APIRouter, Body
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms_schema import RoomPATCH, RoomAdd
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/rooms", tags=["Комнаты"])


@router.get("", summary="Получение списка комнат отеля")
async def get_room(
        pagination: PaginationDep,
        room_id: str | None = Query(None, description="Ид комнаты"),
        title: str | None = Query(None, description="Название Комнаты"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            room_id=room_id,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get("/{room_id}", summary="Получить информацию по комнате")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_non(id=room_id)


@router.post("",
             summary="Добавление комнаты")
async def create_room(
        room_data: RoomAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "hotel_id": "6",
                        "title": "2х местная, люкс",
                        "cost": "1500",
                        "quantity": "3",
                        "description": "Отель находится в уютном районе города, включая прекрасные пляжи",
                    }
                },
            })
):
    async with async_session_maker() as session:
        await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK"}


@router.put("/{room_id}",
            summary="Полное изменение отеля",
            description="<h1>Тут мы полностью обновляем данные об отеле</h1>")
async def edit_room(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
        return {"status": "OK"}


@router.delete("/{room_id}", summary="Удаление выбранного отеля")
async def delete_hotel(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
        return {"status": "OK"}


@router.patch(
    "/{room_id}",
    summary="Частичное обновление данных о комнате",
    description="<h1>Тут мы частично обновляем данные о комнате</h1>",
)
async def partially_edit_room(room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
        return {"status": "OK"}
