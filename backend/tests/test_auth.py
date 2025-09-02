from httpx import Client


def test_register_and_login(client: Client, db_session):
    response = client.post("/register", json={"email": "user@example.com", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()

    response = client.post("/login", json={"email": "user@example.com", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()
