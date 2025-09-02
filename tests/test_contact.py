from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_contact_success():
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "message": "Hello",
        "device_id": "dev123",
    }
    response = client.post("/api-v1/contact", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_contact_validation_error():
    payload = {
        "name": "Bob",
        "email": "not-an-email",
        "message": "Hi",
        "device_id": "dev321",
    }
    response = client.post("/api-v1/contact", json=payload)
    assert response.status_code == 422
    assert response.json() == {"status": 422, "message": "Validation Error"}
