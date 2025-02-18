from fastapi import Query, HTTPException, APIRouter, Body, Depends
from sqlalchemy import insert, select, func
from src.database import async_session_maker
from src.schemas.hotels_schema import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsORrm

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Локация отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsORrm)
        if title:
            query = query.filter(func.lower(HotelsORrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsORrm.location).contains(location.strip().lower()))

        query = query.limit(per_page).offset(per_page * (pagination.page - 1)
                                             )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        all_hotels = result.scalars().all()

        return all_hotels


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
        add_hotel_stmt = insert(HotelsORrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}",
            summary="Полное изменение отеля",
            description="<h1>Тут мы полностью обновляем данные об отеле </h1>", )
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = next((hotel for hotel in hotels if hotel["id"] == hotel_id), None)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Отель не найден")
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK", "new_hotel_info": hotel}


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
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
