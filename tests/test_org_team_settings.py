from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
API_PREFIX = "/api-v1"


def test_org_team_settings_endpoints():
    # Org endpoints
    res = client.get(f"{API_PREFIX}/org/me")
    assert res.status_code == 200
    res = client.patch(f"{API_PREFIX}/org", json={"plan": "pro", "acknowledge": True})
    assert res.status_code == 200
    assert res.json()["plan"] == "pro"

    # Team endpoints
    create = client.post(
        f"{API_PREFIX}/team",
        json={"orgId": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
    )
    assert create.status_code == 200
    member_id = create.json()["id"]

    res = client.get(f"{API_PREFIX}/team", params={"orgId": 1})
    assert res.status_code == 200
    assert len(res.json()) == 1

    res = client.patch(f"{API_PREFIX}/team/{member_id}", json={"active": False})
    assert res.status_code == 200
    assert res.json()["active"] is False

    res = client.delete(f"{API_PREFIX}/team/{member_id}")
    assert res.status_code == 200

    # Settings endpoints
    tariffs_payload = {
        "rate_hour": 50,
        "min_minutes": 30,
        "step_minutes": 15,
        "markup_percent": 10,
        "vat_percent": 20,
        "travel_per_km": 0.5,
    }
    res = client.put(f"{API_PREFIX}/settings/tariffs", json=tariffs_payload)
    assert res.status_code == 200

    res = client.put(
        f"{API_PREFIX}/settings/provider", json={"default_provider": "prov"}
    )
    assert res.status_code == 200

    res = client.post(
        f"{API_PREFIX}/settings/provider/catalog", json={"file": "cat.csv"}
    )
    assert res.status_code == 200

    prefixes_payload = {
        "quote_prefix": "Q",
        "invoice_prefix": "I",
        "work_prefix": "W",
        "reset": {"quote_next": 1, "invoice_next": 1, "work_next": 1},
    }
    res = client.put(f"{API_PREFIX}/settings/prefixes", json=prefixes_payload)
    assert res.status_code == 200

    fiscal_payload = {
        "legal_name": "Acme",
        "tax_id": "123",
        "address": "Main",
        "city_zip": "City 123",
    }
    res = client.put(f"{API_PREFIX}/settings/fiscal", json=fiscal_payload)
    assert res.status_code == 200

    res = client.post(
        f"{API_PREFIX}/settings/branding/logo", json={"file": "logo.png"}
    )
    assert res.status_code == 200

    branding_payload = {"invoice_template": "inv", "quote_template": "quote"}
    res = client.put(f"{API_PREFIX}/settings/branding", json=branding_payload)
    assert res.status_code == 200

    res = client.get(f"{API_PREFIX}/settings/branding/preview")
    assert res.status_code == 200

    email_payload = {"subject": "Hi", "body": "Hello"}
    res = client.put(f"{API_PREFIX}/settings/email-template", json=email_payload)
    assert res.status_code == 200

    res = client.post(
        f"{API_PREFIX}/settings/ai/uploads", json={"files": ["a.txt"]}
    )
    assert res.status_code == 200

    assert client.post(f"{API_PREFIX}/settings/ai/train").status_code == 200
    assert client.get(f"{API_PREFIX}/settings/ai/status").status_code == 200
    assert client.post(f"{API_PREFIX}/settings/ai/reset").status_code == 200
    assert client.get(f"{API_PREFIX}/settings/ai/model").status_code == 200

    res = client.get(f"{API_PREFIX}/settings")
    assert res.status_code == 200
