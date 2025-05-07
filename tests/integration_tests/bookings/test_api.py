import pytest
from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    ("hotel_id", "room_id", "date_from", "date_to", "status_code"),
    [
        (1, 1, "2025-03-28", "2025-03-30", 200),
        (1, 1, "2025-03-28", "2025-03-30", 200),
        (1, 1, "2025-03-28", "2025-04-01", 200),
        (1, 1, "2025-03-29", "2025-04-07", 200),
        (1, 1, "2025-03-28", "2025-04-02", 200),
        (1, 1, "2025-03-28", "2025-04-12", 409),
    ],
)
async def test_add_booking(
        authenticated_ac, hotel_id, room_id, date_from, date_to, status_code
):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "hotel_id": hotel_id,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    if status_code == 200:
        assert response.status_code == status_code
        res = response.json()
        assert isinstance(res, dict)


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for db_ in get_db_null_pool():
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize(
    ("hotel_id", "room_id", "date_from", "date_to", "booked_rooms"),
    [
        (1, 1, "2025-03-28", "2025-03-30", 1),
        (1, 1, "2025-03-28", "2025-03-30", 2),
        (1, 1, "2025-03-28", "2025-04-01", 3),
    ],
)
async def test_add_and_get_booking(
        hotel_id,
        room_id,
        date_from,
        date_to,
        booked_rooms,
        delete_all_bookings,
        authenticated_ac,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "hotel_id": hotel_id,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200
    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == booked_rooms
