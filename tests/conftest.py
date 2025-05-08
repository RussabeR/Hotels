# ruff: noqa: E402
import json
from collections.abc import AsyncGenerator
from unittest import mock

from src.api.dependencies import get_db

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.database import Base, async_session_maker_null_pool, engine
from src.main import app
from src.models import *  # noqa
from src.schemas.hotels_schema import HotelAdd
from src.schemas.rooms_schema import RoomAdd
from src.schemas.facilities_schema import FacilityAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> AsyncGenerator[DBManager]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("База дропнута")
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы созданы")

    with open("tests/jsons/mock_hotels.json", "r", encoding="utf-8") as file:
        hotels = json.load(file)

    with open("tests/jsons/mock_rooms.json", "r", encoding="utf-8") as file:
        rooms = json.load(file)

    with open("tests/jsons/mock_facilities.json", "r", encoding="utf-8") as file:
        facilities = json.load(file)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]
    facilities = [FacilityAdd.model_validate(facility) for facility in facilities]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.facilities.add_bulk(facilities)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_test_user(ac, setup_database) -> AsyncClient:
    await ac.post(
        "/auth/register", json={"email": "sobaka@gmail.com", "password": "12345"}
    )
    return ac


@pytest.fixture(scope="session")
async def authenticated_ac(ac, register_test_user):
    await ac.post(
        "/auth/login", json={"email": "sobaka@gmail.com", "password": "12345"}
    )
    assert ac.cookies["access_token"]
    yield ac
