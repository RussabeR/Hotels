from fastapi import APIRouter, HTTPException, Response, Request

from src.repositories.services.auth import AuthService
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users_schema import UserRequestAdd, UserAdd

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post("/register", summary="Регистрация нового пользователя")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}


@router.post("/login", summary="Войти")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)

        if user is None:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        access_token = AuthService().create_access_token({'user_id': user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/only_auth", summary="Получить токен текущего пользователя")
async def only_auth(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return {"error": "No access token found"}

    return {"access_token": access_token}
