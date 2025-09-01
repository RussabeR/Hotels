import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("CAT@gmail.com", "12345", 200),
        ("CAT1@gmail.com", "12345", 200),
        ("CAT@gmail.com", "12345", 409),
        ("abc2", "12345", 422),
    ],
)
async def test_auth_flow(email: str, password: int, status_code: int, ac):
    # /registration
    resp_register = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert resp_register.status_code == status_code
    if status_code != 200:
        return

    # /Login
    resp_login = await ac.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert resp_login.status_code == 200
    assert ac.cookies["access_token"]
    assert "access_token" in resp_login.json()

    # /me
    resp_me = await ac.get("auth/me")
    assert resp_me.status_code == 200
    user = resp_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /Logout
    resp_logout = await ac.post("auth/logout")
    assert resp_logout.status_code == 200
    assert "access_token" not in ac.cookies
