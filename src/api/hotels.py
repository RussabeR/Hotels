from fastapi import Query, HTTPException, APIRouter, Body, Depends
from sqlalchemy import insert, select, func

from repositories.hotels import HotelsRepository

from src.database import async_session_maker
from src.schemas.hotels_schema import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Локация отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all()
    # per_page = pagination.per_page or 5
    # async with async_session_maker() as session:
    #     query = select(HotelsORrm)
    #     if title:
    #         query = query.filter(func.lower(HotelsORrm.title).contains(title.strip().lower()))
    #     if location:
    #         query = query.filter(func.lower(HotelsORrm.location).contains(location.strip().lower()))
    #
    #     query = query.limit(per_page).offset(per_page * (pagination.page - 1)
    #                                          )
    #     print(query.compile(compile_kwargs={"literal_binds": True}))
    #     result = await session.execute(query)
    #     all_hotels = result.scalars().all()
    #
    #     return all_hotels


@router.post("",
             summary="Добавление нового отеля")
async def create_hotel(
        hotel_data: Hotel = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Отель Сочи 5 звезд у моря",
                        "location": "sochi_u_morya",
                    }
                },
                "2": {
                    "summary": "Дубай",
                    "value": {
                        "title": "Отель Дубай У фонтана",
                        "location": "dubai_fountain",
                    }
                }
            })
):
    async with async_session_maker() as session:
        await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel_data}


@router.put("/{hotel_id}",
            summary="Полное изменение отеля",
            description="<h1>Тут мы полностью обновляем данные об отеле</h1>")
async def update_hotel(
        hotel_id: int,
        hotel_data: Hotel = Body()
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).update(hotel_id, hotel_data)
        await session.commit()
        return {"status": "OK", "data": hotel}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
def partially_edit_hotel(
        hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление выбранного отеля")
async def delete_hotel(
        hotel_data: Hotel = Body()
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(hotel_data)
        await session.commit()
        return {"status": "OK"}
