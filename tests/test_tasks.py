# dummy1
# dummy2
from fastapi.testclient import TestClient
from main import app
from backend.api.models.user import User
from backend.api.routers.auth import create_access_token

client = TestClient(app)

# Versioned API prefix used for all task endpoints.
API_PREFIX = "/api-v1"


def create_user(db, device_id: str = "testdevice"):
    user = User(email="user@example.com", hashed_password="pwd", device_id=device_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id), "device_id": device_id})
    return user, token


def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_create_and_list_tasks(db_session):
    user, token = create_user(db_session)
    response = client.post(
        f"{API_PREFIX}/tasks",
        json={"title": "Test", "description": "desc"},
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["owner_id"] == user.id

    resp = client.get(f"{API_PREFIX}/tasks", headers=auth_headers(token))
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == data["id"]


def test_update_and_delete_task(db_session):
    user, token = create_user(db_session)
    create_resp = client.post(
        f"{API_PREFIX}/tasks",
        json={"title": "Task", "description": None},
        headers=auth_headers(token),
    )
    task_id = create_resp.json()["id"]

    update_resp = client.patch(
        f"{API_PREFIX}/tasks/{task_id}",
        json={"title": "Updated"},
        headers=auth_headers(token),
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Updated"

    delete_resp = client.delete(
        f"{API_PREFIX}/tasks/{task_id}", headers=auth_headers(token)
    )
    assert delete_resp.status_code == 200

    list_resp = client.get(f"{API_PREFIX}/tasks", headers=auth_headers(token))
    assert list_resp.status_code == 200
    assert list_resp.json() == []
