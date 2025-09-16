from typing import Any, Dict, Final
from fastapi.testclient import TestClient
from httpx import Response
from api.models.schemas.user_schemas import CreateUserDTO, UpdateUserDTO, LoginDTO
import random

def create_user_return_token(client: TestClient):
    num: Final[int] = random.randint(1,1000000000)

    json_dto = CreateUserDTO(
        name = f"user {num}",
        email = f"user{num}@example.com",
        password = str(num)
    )

    model: Final[Dict[str, Any]] = dict(json_dto)

    response: Final[Response] = client.post(
        "/api/v1/auth/register",
        json=model
    )

    assert response.status_code == 201
    response_data = response.json()
    
    assert response_data['body']['token'] is not None

    return {
        "token": response_data['body']['token'], 
        "dto": json_dto
        }

def test_get_user(client: TestClient):
    response: Final = create_user_return_token(client)

    response_get: Final[Response] = client.get(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {response['token']}"},
    )

    assert response_get.status_code == 200

    response_get_data: Final = response_get.json()

    assert response_get_data['code'] == 200
    assert response_get_data['message'] == "User found with successfully"
    assert response_get_data['status'] == True
    assert response_get_data['body']['id'] == response_get_data['body']['id']
    assert response_get_data['body']['name'] == response_get_data['body']['name']
    assert response_get_data['body']['email'] == response_get_data['body']['email']

def test_update_user(client: TestClient):
    response: Final = create_user_return_token(client)

    dto: Final[UpdateUserDTO] = UpdateUserDTO(
        name = "user updated",
        password = None
    )
    
    response_put: Final[Response] = client.put(
        "/api/v1/user",
        json=dict(dto),
        headers={"Authorization": f"Bearer {response['token']}"},
    )

    assert response_put.status_code == 200

    response_get_data: Final = response_put.json()

    assert response_get_data['code'] == 200
    assert response_get_data['message'] == "User updated with successfully"
    assert response_get_data['status'] == True
    assert response_get_data['body']['name'] == dto.name

def test_delete_user(client: TestClient):
    response: Final = create_user_return_token(client)

    response_get: Final[Response] = client.delete(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {response['token']}"},
    )

    assert response_get.status_code == 200

    response_get_data: Final = response_get.json()

    assert response_get_data['code'] == 200
    assert response_get_data['message'] == "See you later"
    assert response_get_data['status'] == True
    assert response_get_data['body'] is None