from datetime import date
from fastapi_cache.decorator import cache
from fastapi import Query, APIRouter, Body

from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
    handle_room_and_hotel_exceptions, check_actual_dates,
)
from src.schemas.hotels_schema import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/all", summary="Получение списка всех отелей (Администратору)")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("", summary="Получение списка свободных отелей")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(examples="2025-03-06"),
        date_to: date = Query(examples="2025-03-29"),
):
    check_actual_dates(date_from, date_to)

    hotels = await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )
    return hotels


@router.get("/{hotel_id}", summary="Получение информации по отелю")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="Добавление нового отеля")
@handle_room_and_hotel_exceptions
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Отель Сочи 5 звезд у моря",
                        "location": "sochi_u_morya",
                    },
                },
                "2": {
                    "summary": "Дубай",
                    "value": {
                        "title": "Отель Дубай У фонтана",
                        "location": "dubai_fountain",
                    },
                },
            }
        ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Полное изменение отеля",
    description="<h1>Тут мы полностью обновляем данные об отеле</h1>",
)
@handle_room_and_hotel_exceptions
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление выбранного отеля")
@handle_room_and_hotel_exceptions
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
@handle_room_and_hotel_exceptions
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await HotelService(db).partially_edit_hotel(
        hotel_id, hotel_data, exclude_unset=True
    )
    return {"status": "OK"}
