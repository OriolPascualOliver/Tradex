from fastapi.testclient import TestClient
from jose import jwt
from main import app
from backend.api.routers.auth import SECRET_KEY, ALGORITHM
from backend.api.models.user import User

client = TestClient(app)


def register_user(
    email: str = "user@example.com",
    password: str = "secret",
    device_id: str = "device_register",
):
    return client.post(
        "/api-v1/auth/register",
        json={"email": email, "password": password, "device_id": device_id},
    )


def login_user(
    email: str = "user@example.com",
    password: str = "secret",
    device_id: str = "device_login",
):
    return client.post(
        "/api-v1/auth/login",
        json={"email": email, "password": password, "device_id": device_id},
    )


def forgot_password(email: str = "user@example.com", device_id: str = "device_forgot"):
    return client.post(
        "/api-v1/auth/forgotpassword", json={"email": email, "device_id": device_id}
    )


def reset_password(token: str, new_password: str, device_id: str = "device_forgot"):
    return client.post(
        "/api-v1/auth/reset",
        json={"token": token, "new_password": new_password, "device_id": device_id},
    )


def test_register_and_login(db_session):
    register_device = "device_register"
    login_device = "device_login"

    response = register_user(device_id=register_device)
    assert response.status_code == 200
    token = response.json()["access_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["device_id"] == register_device
    user = db_session.query(User).filter(User.email == "user@example.com").first()
    assert user.device_id == register_device

    response = login_user(device_id=login_device)
    assert response.status_code == 200
    token = response.json()["access_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["device_id"] == login_device
    user = db_session.query(User).filter(User.email == "user@example.com").first()
    assert user.device_id == login_device


def test_forgot_and_reset(db_session):
    register_user(device_id="device_initial")

    forgot_device = "device_forgot"
    response = forgot_password(device_id=forgot_device)
    assert response.status_code == 200
    token = response.json()["reset_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["device_id"] == forgot_device
    user = db_session.query(User).filter(User.email == "user@example.com").first()
    assert user.device_id == forgot_device

    response = reset_password(token, "newsecret", device_id=forgot_device)
    assert response.status_code == 200
    user = db_session.query(User).filter(User.email == "user@example.com").first()
    assert user.device_id == forgot_device

    # login with new password
    new_login_device = "device_new_login"
    response = login_user(password="newsecret", device_id=new_login_device)
    assert response.status_code == 200
    payload = jwt.decode(response.json()["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["device_id"] == new_login_device
    user = db_session.query(User).filter(User.email == "user@example.com").first()
    assert user.device_id == new_login_device

    # old password should fail
    response = login_user(password="secret", device_id="invalid")
    assert response.status_code == 400
