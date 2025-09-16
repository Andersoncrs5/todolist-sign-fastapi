from typing import Any, Dict, Final
from fastapi.testclient import TestClient
from httpx import Response
from api.models.schemas.user_schemas import CreateUserDTO, LoginDTO
import random


def test_login_user(client: TestClient):
    num: Final[int] = random.randint(1,1000000000)

    model: Final[Dict[str, Any]] = dict(CreateUserDTO(
        name = f"user {num}",
        email = f"user{num}@example.com",
        password = str(num)
    ))

    response_create: Final[Response] = client.post(
        "/api/v1/auth/register",
        json=model
    )

    assert response_create.status_code == 201

    model_log: Final[Dict[str, Any]] = dict(LoginDTO(
        email = model['email'],
        password = model['password'],
    ))

    response_login: Final[Response] = client.post(
        "/api/v1/auth/login",
        json=model_log
    )

    assert response_login.status_code == 200
    response_data: Final = response_login.json()

    assert response_data['message'] == 'Welcome again'
    assert response_data['code'] == 200
    assert response_data['status'] == True
    assert response_data['body']['token'] is not None
    assert response_data['body']['refresh_token'] is not None
    assert response_data['datetime'] is not None

def test_create_new_user(client: TestClient):
    num: Final[int] = random.randint(1,1000000000)

    model: Final[Dict[str, Any]] = dict(CreateUserDTO(
        name = f"user {num}",
        email = f"user{num}@example.com",
        password = str(num)
    ))

    response: Final[Response] = client.post(
        "/api/v1/auth/register",
        json=model
    )

    assert response.status_code == 201
    response_data = response.json()

    assert response_data['message'] == 'Welcome'
    assert response_data['code'] == 201
    assert response_data['status'] == True
    assert response_data['body']['token'] is not None
    assert response_data['body']['refresh_token'] is not None
    assert response_data['datetime'] is not None