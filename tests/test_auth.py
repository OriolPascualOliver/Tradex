from fastapi.testclient import TestClient
from jose import jwt
from main import app
from backend.api.routers.auth import SECRET_KEY, ALGORITHM
from backend.api.models.user import User

client = TestClient(app)

# All authentication endpoints are served under a versioned API prefix.
API_PREFIX = "/api-v1"


def register_user(
    email: str = "user@example.com",
    password: str = "secret",
    device_id: str = "device_register",
):
    payload = {
        "license": "solo",
        "team_members": 1,
        "email": email,
        "telephone": "123456789",
        "first_name": "John",
        "surname1": "Doe",
        "surname2": "Smith",
        "nif": "12345678A",
        "password": password,
        "confirm_password": password,
        "company_name": "Acme",
        "sector": "Tech",
        "country": "ES",
        "state": "Madrid",
        "zip_code": "28001",
        "terms_accepted": True,
        "device_id": device_id,
    }
    return client.post(f"{API_PREFIX}/auth/register", json=payload)


def login_user(
    email: str = "user@example.com",
    password: str = "secret",
    device_id: str = "device_login",
):
    return client.post(
        f"{API_PREFIX}/auth/login",
        json={"email": email, "password": password, "device_id": device_id},
    )


def forgot_password(email: str = "user@example.com", device_id: str = "device_forgot"):
    return client.post(
        f"{API_PREFIX}/auth/forgotpassword", json={"email": email, "device_id": device_id}
    )


def reset_password(token: str, new_password: str, device_id: str = "device_forgot"):
    return client.post(
        f"{API_PREFIX}/auth/reset",
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
    assert user.last_login is not None
    first_login = user.last_login
    assert user.sign_in_date is None

    response = login_user(device_id=login_device)
    assert response.status_code == 200
    token = response.json()["access_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["device_id"] == login_device
    user = db_session.query(User).filter(User.email == "user@example.com").first()
    assert user.device_id == login_device
    assert user.last_login > first_login
    assert user.sign_in_date is not None
    first_sign_in = user.sign_in_date

    # second login should not change sign_in_date
    response = login_user(device_id="device_login2")
    assert response.status_code == 200
    user = db_session.query(User).filter(User.email == "user@example.com").first()
    assert user.sign_in_date == first_sign_in


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
    assert user.last_login is not None

    # old password should fail
    response = login_user(password="secret", device_id="invalid")
    assert response.status_code == 400
