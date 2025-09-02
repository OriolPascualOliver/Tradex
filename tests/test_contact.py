from fastapi.testclient import TestClient
from main import app
from backend.api.routers import contact as contact_router

client = TestClient(app)

# Base prefix for all versioned API routes.
API_PREFIX = "/api-v1"


def test_contact_success(monkeypatch):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "message": "Hello",
        "device_id": "dev123",
    }

    called = {}

    def fake_send_email(name, email, message, device_id):
        called["args"] = (name, email, message, device_id)

    monkeypatch.setattr(contact_router, "send_email", fake_send_email)

    response = client.post(f"{API_PREFIX}/contact", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert called["args"] == (
        "Alice",
        "alice@example.com",
        "Hello",
        "dev123",
    )


def test_contact_validation_error():
    payload = {
        "name": "Bob",
        "email": "not-an-email",
        "message": "Hi",
        "device_id": "dev321",
    }
    response = client.post(f"{API_PREFIX}/contact", json=payload)
    assert response.status_code == 422
    assert response.json() == {"status": 422, "message": "Validation Error"}


def test_contact_missing_device_id():
    payload = {
        "name": "Eve",
        "email": "eve@example.com",
        "message": "Hi",
    }
    response = client.post(f"{API_PREFIX}/contact", json=payload)
    assert response.status_code == 422
    assert response.json() == {"status": 422, "message": "Validation Error"}
