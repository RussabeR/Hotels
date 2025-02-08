from fastapi import Query, HTTPException, APIRouter, Body
from schemas.hotels_schema import Hotel, HotelPATCH
from typing import List, Dict, Any

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("", summary="Получение информации об отеле")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        page: int = Query(1, description="Номер страницы"),
        per_page: int = Query(3, description="Количество отелей на странице"),
) -> Dict[str, Any]:
    # Фильтруем отели по id и title
    filtered_hotels = [
        hotel for hotel in hotels
        if (id is None or hotel["id"] == id) and (title is None or hotel["title"] == title)
    ]

    # Пагинация (срез списка)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_hotels = filtered_hotels[start:end]

    return {
        "page": page,
        "per_page": per_page,
        "total": len(filtered_hotels),
        "hotels": paginated_hotels
    }


@router.post("",
             summary="Добавление нового отеля")
def create_hotel(
        hotel_data: Hotel = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Отель Сочи 5 звезд у моря",
                        "name": "sochi_u_morya",
                    }
                },
                "2": {
                    "summary": "Дубай",
                    "value": {
                        "title": "Отель Дубай У фонтана",
                        "name": "dubai_fountain",
                    }
                }
            })
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK", "hotel": hotels[-1]}


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
