import json

import pytest
from httpx import ASGITransport, AsyncClient
from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope='session', autouse=True)
async def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope='session', autouse=True)
async def async_main(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await  conn.run_sync(Base.metadata.drop_all)
        await  conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
async def create_hotels_test(check_test_mode):
    with open("tests/jsons/mock_hotels.json", "r", encoding="utf-8") as file:
        hotels_data = json.load(file)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for hotel in hotels_data:
            await ac.post("/hotels", json=hotel)


@pytest.fixture(scope='session')
async def create_rooms_test(create_hotels_test):
    with open("tests/jsons/mock_rooms.json", "r", encoding="utf-8") as file:
        rooms_data = json.load(file)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for room in rooms_data:
            await ac.post("/{hotel_id}/rooms", json=room)


@pytest.fixture(scope='session', autouse=True)
async def register_test_user(create_rooms_test):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post("/auth/register",
                      json={
                          "email": "sobaka@gmail.com",
                          "password": "12345"}
                      )
