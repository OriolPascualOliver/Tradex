from fastapi.testclient import TestClient
from main import app
from backend.api.models.user import User

client = TestClient(app)

# Versioned API prefix used for all task endpoints.
API_PREFIX = "/api-v1"


def create_user(db):
    user = User(email="user@example.com", hashed_password="pwd")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_create_and_list_tasks(db_session):
    user = create_user(db_session)
    response = client.post(
        f"{API_PREFIX}/tasks",
        json={"title": "Test", "description": "desc"},
        headers={"X-User-Id": str(user.id)},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["owner_id"] == user.id

    resp = client.get(f"{API_PREFIX}/tasks", headers={"X-User-Id": str(user.id)})
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == data["id"]


def test_update_and_delete_task(db_session):
    user = create_user(db_session)
    create_resp = client.post(
        f"{API_PREFIX}/tasks",
        json={"title": "Task", "description": None},
        headers={"X-User-Id": str(user.id)},
    )
    task_id = create_resp.json()["id"]

    update_resp = client.patch(
        f"{API_PREFIX}/tasks/{task_id}",
        json={"title": "Updated"},
        headers={"X-User-Id": str(user.id)},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Updated"

    delete_resp = client.delete(
        f"{API_PREFIX}/tasks/{task_id}", headers={"X-User-Id": str(user.id)}
    )
    assert delete_resp.status_code == 200

    list_resp = client.get(f"{API_PREFIX}/tasks", headers={"X-User-Id": str(user.id)})
    assert list_resp.status_code == 200
    assert list_resp.json() == []
