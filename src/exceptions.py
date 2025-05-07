from datetime import date
from functools import wraps

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
    detail = "Отель не найден"


class UserAlreadyExistException(NabronirovalAppException):
    status_code = 409
    detail = "Такой пользователь уже существует"


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


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


class EmailAlreadyExistHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с таким Email уже зарегистрирован"


class WrongPasswordHTTPException(NabronirovalHTTPException):
    statuscode = 409
    detail = "Неверный пароль"


def check_dates_from_dates_to(date_to: date, date_from: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422, detail="Дата выезда не может быть ровна/ раньше въезда"
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
