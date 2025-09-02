from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

API_PREFIX = "/api-v1"


def test_health():
    response = client.get(f"{API_PREFIX}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
