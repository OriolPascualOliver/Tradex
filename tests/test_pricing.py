from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

API_PREFIX = "/api-v1"


def test_pricing_endpoint():
    response = client.get(f"{API_PREFIX}/pricing")
    assert response.status_code == 200
    data = response.json()
    assert data["currency"] == "EUR"
    assert "solo" in data and "team" in data
    assert isinstance(data["team"]["tiers"], list) and len(data["team"]["tiers"]) > 0
