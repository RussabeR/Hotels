from fastapi import APIRouter, Response, Request
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    EmailAlreadyExistHTTPException, EmptyPasswordHTTPException, AuthOutHTTPException,
    InvalidAuthHTTPException, ShortPasswordHTTPException,
)
from src.services.auth import AuthService
from src.schemas.users_schema import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация нового пользователя")
async def register_user(data: UserRequestAdd, db: DBDep):
    if not data.password.strip():
        raise EmptyPasswordHTTPException
    if len(data.password.strip()) < 8:
        raise ShortPasswordHTTPException
    try:
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await db.users.add(new_user_data)
        await db.commit()
    except Exception as e:
        print(e)  # noqa
        raise EmailAlreadyExistHTTPException
    return {"status": "OK"}


@router.post("/login", summary="Войти")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if user is None:
        raise InvalidAuthHTTPException
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise InvalidAuthHTTPException

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получить токен текущего пользователя")
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout", summary="Выйти из системы")
async def logout(response: Response, request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise AuthOutHTTPException
    response.delete_cookie("access_token")
    return {"status": "Вы вышли из системы"}
