async def test_api(ac):
    response = await ac.get(
        "/hotels", params={"date_from": "2025-03-26", "date_to": "2025-03-30"}
    )
    print(f"{response=}")

    assert response.status_code == 200
