from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def register_user(email: str = "user@example.com", password: str = "secret"):
    return client.post(
        "/api-v1/auth/register", json={"email": email, "password": password}
    )


def login_user(email: str = "user@example.com", password: str = "secret"):
    return client.post(
        "/api-v1/auth/login", json={"email": email, "password": password}
    )


def forgot_password(email: str = "user@example.com"):
    return client.post("/api-v1/auth/forgotpassword", json={"email": email})


def reset_password(token: str, new_password: str):
    return client.post(
        "/api-v1/auth/reset", json={"token": token, "new_password": new_password}
    )


def test_register_and_login(db_session):
    response = register_user()
    assert response.status_code == 200
    assert "access_token" in response.json()

    response = login_user()
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_forgot_and_reset(db_session):
    register_user()
    response = forgot_password()
    assert response.status_code == 200
    token = response.json()["reset_token"]

    response = reset_password(token, "newsecret")
    assert response.status_code == 200

    # login with new password
    response = login_user(password="newsecret")
    assert response.status_code == 200

    # old password should fail
    response = login_user(password="secret")
    assert response.status_code == 400
