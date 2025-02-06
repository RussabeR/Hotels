from fastapi import FastAPI, HTTPException
from typing import Optional
import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI()


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


hotels_db = {
    '1': {'title': 'Luxury Suites - Exclusive 5-star experience', 'name': 'The Lavender Inn'}
}


@app.get("/hotels/{hotel_id}")
def get_info(hotel_id: str):
    if hotel_id in hotels_db:
        return f'Информация об отеле с id {hotel_id}: {hotels_db[hotel_id]}'
    else:
        raise HTTPException(status_code=404, detail=f'Отель с id {hotel_id} не найден!')


@app.put("/hotels/{hotel_id}")
def add_hotel_info(hotel_id: str, title: str, name: str):
    if hotel_id in hotels_db:
        return {"Ошибка": f'Отель с id {hotel_id} уже существует!'}

    hotels_db[hotel_id] = {'title': title, 'name': name}
    return {f'Добавлен новый отель: {hotel_id} - {hotels_db[hotel_id]}'}


@app.patch("/hotels/{hotel_id}")
def change_hotel_info(hotel_id: str, title: Optional[str] = None, name: Optional[str] = None):
    if hotel_id not in hotels_db:
        raise HTTPException(status_code=404, detail=f'Отель с id {hotel_id} не найден!')

    updates = []

    if title:
        hotels_db[hotel_id]["title"] = title
        updates.append(f"Заголовок изменен на - {title}")

    if name:
        hotels_db[hotel_id]["name"] = name
        updates.append(f"Имя изменено на {name}")

    if updates:
        return {f'Изменения для id отеля {hotel_id} применены : {updates} - {hotels_db[hotel_id]}'}

    return {"message": f"Нет изменений для отеля : {hotel_id}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
