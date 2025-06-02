from datetime import date
from functools import wraps
from src.config import settings

from fastapi import HTTPException


class NabronirovalAppException(Exception):
    details = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)


class InvalidTokenException(NabronirovalAppException):
    details = "Неверный токен"


class ObjectNotFoundException(NabronirovalAppException):
    details = "Объект не найден"


class NoAvailableRoomsException(NabronirovalAppException):
    status_code = 409
    details = "Не осталось свободных номеров"


class ObjectExistYet(NabronirovalAppException):
    details = "Объект уже существует"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class FacilityNotFoundException(ObjectNotFoundException):
    detail = "Удобство не найдено"


class UserAlreadyExistException(NabronirovalAppException):
    detail = "Такой пользователь уже существует"


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class EmptyPasswordHTTPException(NabronirovalAppException):
    detail = "Пароль не может быть пустым"


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class HotelDateHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Неверная дата заезда"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"


class FacilityNotFoundHTTPException(NabronirovalHTTPException):
    detail = "Удобство не найдено"


class NoAvailableRoomsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class UserAlreadyExistHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Такой пользователь уже существует"


class EmptyPasswordHTTPException(NabronirovalHTTPException):
    status_code = 400
    detail = "Пароль не может быть пустым"


class ShortPasswordHTTPException(NabronirovalHTTPException):
    status_code = 400
    detail = "Пароль должен быть не менее 8 символов"


class EmailAlreadyExistHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с таким Email уже зарегистрирован"


class InvalidAuthHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Неверный Email или пароль"


class AuthOutHTTPException(NabronirovalHTTPException):
    status_code = 403
    detail = "Выполните авторизацию"


class FacilitiesNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Введен несуществующий id Удобств"


def check_dates_from_dates_to(date_to: date, date_from: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422, detail="Дата выезда не может быть ровна/ раньше въезда"
        )


def check_actual_dates(date_from: date, date_to: date) -> None:
    actual_date = date.today()
    if date_from < actual_date:
        raise HTTPException(
            status_code=422,
            detail="Дата заезда не может быть в прошлом"
        )

    if date_to <= date_from:
        raise HTTPException(
            status_code=422,
            detail="Дата выезда должна быть позже даты заезда"
        )

    if (date_to - actual_date).days > settings.MAX_BOOKING_DAYS_AHEAD:
        raise HTTPException(
            status_code=422,
            detail=f"Дата выезда не может быть позже чем через {settings.MAX_BOOKING_DAYS_AHEAD} дней"
        )


def handle_room_and_hotel_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RoomNotFoundException:
            raise RoomNotFoundHTTPException()
        except HotelNotFoundException:
            raise HotelNotFoundHTTPException()

    return wrapper
