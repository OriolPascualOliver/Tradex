from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
API_PREFIX = "/api-v1"


def test_clock_endpoint():
    payload = {"taskID": 0, "direction": "in", "deviceid": "dev1"}
    r = client.post(f"{API_PREFIX}/auth/clock", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "clocked in"
    payload.update({"taskID": 1, "direction": "out"})
    r = client.post(f"{API_PREFIX}/auth/clock", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "clocked out"


def test_org_and_team():
    r = client.get(f"{API_PREFIX}/org/me")
    assert r.status_code == 200
    assert r.json()["plan"] == "free"
    r = client.patch(
        f"{API_PREFIX}/org",
        json={"plan": "pro", "acknowledge": True, "teamMembers": 3},
    )
    assert r.status_code == 200
    assert r.json()["plan"] == "pro"
    member_payload = {
        "orgId": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "role": "user",
    }
    r = client.post(f"{API_PREFIX}/team", json=member_payload)
    assert r.status_code == 200
    member_id = r.json()["id"]
    r = client.get(f"{API_PREFIX}/team", params={"orgId": 1})
    assert r.status_code == 200
    assert len(r.json()) == 1
    r = client.patch(
        f"{API_PREFIX}/team/{member_id}",
        json={"role": "admin", "active": False},
    )
    assert r.status_code == 200
    assert r.json()["role"] == "admin"
    r = client.delete(f"{API_PREFIX}/team/{member_id}")
    assert r.status_code == 200
    assert r.json()["status"] == "deleted"


def test_settings_endpoints():
    r = client.post(
        f"{API_PREFIX}/settings/ai/uploads",
        json={"files": ["a.txt"]},
    )
    assert r.status_code == 200
    assert r.json()["uploaded"] == 1
    r = client.post(f"{API_PREFIX}/settings/ai/train")
    assert r.status_code == 200
    r = client.get(f"{API_PREFIX}/settings/ai/status")
    assert r.status_code == 200
    r = client.post(f"{API_PREFIX}/settings/ai/reset")
    assert r.status_code == 200
    r = client.get(f"{API_PREFIX}/settings/ai/model")
    assert r.status_code == 200

    tariffs = {
        "rate_hour": 1.0,
        "min_minutes": 15,
        "step_minutes": 5,
        "markup_percent": 10.0,
        "vat_percent": 21.0,
        "travel_per_km": 0.5,
    }
    r = client.put(f"{API_PREFIX}/settings/tariffs", json=tariffs)
    assert r.status_code == 200

    provider = {"default_provider": "acme"}
    r = client.put(f"{API_PREFIX}/settings/provider", json=provider)
    assert r.status_code == 200
    r = client.post(
        f"{API_PREFIX}/settings/provider/catalog",
        json={"file": "c.csv"},
    )
    assert r.status_code == 200

    prefixes = {
        "quote_prefix": "Q-",
        "invoice_prefix": "I-",
        "work_prefix": "W-",
        "reset": {"quote_next": 1, "invoice_next": 1, "work_next": 1},
    }
    r = client.put(f"{API_PREFIX}/settings/prefixes", json=prefixes)
    assert r.status_code == 200

    fiscal = {
        "legal_name": "Acme",
        "tax_id": "123",
        "address": "Main St",
        "city_zip": "City",
    }
    r = client.put(f"{API_PREFIX}/settings/fiscal", json=fiscal)
    assert r.status_code == 200

    r = client.post(
        f"{API_PREFIX}/settings/branding/logo",
        json={"file": "logo.png"},
    )
    assert r.status_code == 200
    branding = {"invoice_template": "inv", "quote_template": "qt"}
    r = client.put(f"{API_PREFIX}/settings/branding", json=branding)
    assert r.status_code == 200
    r = client.get(f"{API_PREFIX}/settings/branding/preview")
    assert r.status_code == 200

    email_template = {"subject": "s", "body": "b"}
    r = client.put(
        f"{API_PREFIX}/settings/email-template",
        json=email_template,
    )
    assert r.status_code == 200

    r = client.get(f"{API_PREFIX}/settings")
    assert r.status_code == 200
    assert "tariffs" in r.json()
