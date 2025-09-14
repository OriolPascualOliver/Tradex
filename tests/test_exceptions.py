from fastapi.testclient import TestClient
from pydantic import BaseModel

from main import app
from backend.core.exceptions import (
    ForbiddenException,
    UnauthorizedException,
    UnprocessableEntityException,
)

client = TestClient(app, raise_server_exceptions=False)


def test_unauthorized_handler():
    @app.get("/unauthorized-test")
    def unauthorized_test():
        raise UnauthorizedException("no auth")

    response = client.get("/unauthorized-test")
    assert response.status_code == 401
    assert response.json() == {"status": 401, "message": "no auth"}


def test_forbidden_handler():
    @app.get("/forbidden-test")
    def forbidden_test():
        raise ForbiddenException("no access")

    response = client.get("/forbidden-test")
    assert response.status_code == 403
    assert response.json() == {"status": 403, "message": "no access"}


def test_unprocessable_entity_handler():
    @app.get("/unprocessable-test")
    def unprocessable_test():
        raise UnprocessableEntityException("bad entity")

    response = client.get("/unprocessable-test")
    assert response.status_code == 422
    assert response.json() == {"status": 422, "message": "bad entity"}


def test_validation_error_handler():
    class Item(BaseModel):
        name: str

    @app.post("/validation-test")
    def validation_test(item: Item):
        return item

    response = client.post("/validation-test", json={"wrong": "value"})
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == 422
    assert data["message"] == "Validation Error"
    assert data["errors"][0]["loc"] == ["body", "name"]


def test_generic_exception_handler():
    @app.get("/generic-error-test")
    def generic_error_test():
        raise Exception("boom")

    response = client.get("/generic-error-test")
    assert response.status_code == 500
    assert response.json() == {"status": 500, "message": "Internal Server Error"}
