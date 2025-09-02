from httpx import Client
from backend.api.models.user import User


def create_user(client: Client, email: str):
    return client.post("/register", json={"email": email, "password": "secret"})


def test_task_lifecycle(client: Client, db_session):
    email = "taskuser@example.com"
    create_user(client, email)
    user = db_session.query(User).filter(User.email == email).first()
    headers = {"X-User-Id": str(user.id)}

    # Create a task
    response = client.post(
        "/v1/tasks", headers=headers, json={"title": "Sample", "description": "desc"}
    )
    assert response.status_code == 200
    task_id = response.json()["id"]

    # List tasks
    response = client.get("/v1/tasks", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Update task
    response = client.patch(
        f"/v1/tasks/{task_id}", headers=headers, json={"title": "Updated"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

    # Delete task
    response = client.delete(f"/v1/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["ok"] is True
