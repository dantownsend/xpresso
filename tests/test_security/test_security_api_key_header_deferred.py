from typing import Any, Dict, Generator

import pytest
from pydantic import BaseModel

from xpresso import App, Dependant, Path, Security
from xpresso.security import APIKeyHeader
from xpresso.testclient import TestClient
from xpresso.typing import Annotated


def get_name() -> str:
    return "key"


class LazyAPIKeyHeader(APIKeyHeader):
    def __init__(self, name: Annotated[str, Dependant(get_name, scope="app")]) -> None:
        super().__init__(name=name)


class User(BaseModel):
    username: str


def get_current_user(oauth_header: Annotated[str, Security(LazyAPIKeyHeader)]):
    user = User(username=oauth_header)
    return user


def read_current_user(current_user: Annotated[User, Dependant(get_current_user)]):
    return current_user


app = App([Path("/users/me", get=read_current_user)])


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


openapi_schema: Dict[str, Any] = {
    "openapi": "3.0.3",
    "info": {"title": "API", "version": "0.1.0"},
    "paths": {
        "/users/me": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                    }
                },
                "security": [{"LazyAPIKeyHeader": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {
            "LazyAPIKeyHeader": {"type": "apiKey", "name": "key", "in": "header"}
        }
    },
}


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_security_api_key(client: TestClient):
    response = client.get("/users/me", headers={"key": "secret"})
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "secret"}


def test_security_api_key_no_key(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}
