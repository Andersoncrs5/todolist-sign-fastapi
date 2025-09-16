from typing import Dict, Final
from fastapi.testclient import TestClient
from api.models.schemas.task_schemas import CreateTaskDTO, UpdateTaskDTO
import random
from tests.integration.test_user_controller import create_user_return_token

def create_task(client: TestClient, token: str):
    num: Final[int] = random.randint(1,1000)

    dto: Final[Dict] = dict(CreateTaskDTO(
        title = f"task {num}",
        description = f"task description {num}",
        is_done = True,
        due_date = None,
        priority = 3
    ))

    response_post: Final = client.post(
        "/api/v1/task",
        json=dto,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response_post.status_code == 201

    return response_post.json()

def test_get_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_task: Final = create_task(client, response_user['token'])

    response_get: Final = client.get(
        f"/api/v1/task/{response_task['body']['id']}",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_get.status_code == 200

    response_post_data: Final[Dict] = response_get.json()

    assert response_post_data['code'] == 200
    assert response_post_data['message'] == "Task found with successfully"
    assert response_post_data['status'] == True
    assert response_post_data['body']['id'] == response_task['body']['id']
    assert response_post_data['body']['title'] == response_task['body']['title']
    assert response_post_data['body']['description'] == response_task['body']['description']
    assert response_post_data['body']['is_done'] == response_task['body']['is_done']
    assert response_post_data['body']['due_date'] == response_task['body']['due_date']
    assert response_post_data['body']['priority'] == response_task['body']['priority']
    assert response_post_data['body']['user_id'] == response_task['body']['user_id']

def test_return_null_get_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_get: Final = client.get(
        f"/api/v1/task/{98685868456}",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_get.status_code == 404

    response_post_data: Final[Dict] = response_get.json()

    assert response_post_data['code'] == 404
    assert response_post_data['message'] == "Task not found"
    assert response_post_data['status'] == False
    assert response_post_data['body'] is None

def test_return_bad_request_get_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_get: Final = client.get(
        f"/api/v1/task/{0}",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_get.status_code == 400

    response_post_data: Final[Dict] = response_get.json()

    assert response_post_data['code'] == 400
    assert response_post_data['message'] == "Task Id is required"
    assert response_post_data['status'] == False
    assert response_post_data['body'] is None

def test_get_all(client: TestClient):
    response_user: Final = create_user_return_token(client)

    create_task(client, response_user['token'])
    create_task(client, response_user['token'])
    create_task(client, response_user['token'])
    create_task(client, response_user['token'])
    create_task(client, response_user['token'])
    create_task(client, response_user['token'])
    create_task(client, response_user['token'])
    create_task(client, response_user['token'])
    create_task(client, response_user['token'])
    create_task(client, response_user['token'])
    create_task(client, response_user['token'])

    response_get_all: Final = client.get(
        "/api/v1/task",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_get_all.status_code == 200
    response_get_all_data = response_get_all.json()

    assert response_get_all_data['total'] == 11
    assert response_get_all_data['page'] == 1

def test_create_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    num: Final[int] = random.randint(1,1000)

    dto: Final[Dict] = dict(CreateTaskDTO(
        title = f"task {num}",
        description = f"task description {num}",
        is_done = True,
        due_date = None,
        priority = 3
    ))

    response_post: Final = client.post(
        "/api/v1/task",
        json=dto,
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_post.status_code == 201

    response_data: Final = response_post.json()

    assert response_data['code'] == 201
    assert response_data['message'] == 'Task created with successfully'
    assert response_data['status'] == True
    assert response_data['body']['title'] == dto['title']
    assert response_data['body']['description'] == dto['description']
    assert response_data['body']['is_done'] == dto['is_done']
    assert response_data['body']['is_done'] == dto['is_done']
    assert response_data['body']['is_done'] == dto['is_done']
    assert response_data['body']['created_at'] is not None

def test_delete_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_task: Final = create_task(client, response_user['token'])

    response_delete: Final = client.delete(
        f"/api/v1/task/{response_task['body']['id']}",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_delete.status_code == 200

    response_post_data: Final[Dict] = response_delete.json()

    assert response_post_data['code'] == 200
    assert response_post_data['message'] == "Task deleted with successfully"
    assert response_post_data['status'] == True
    assert response_post_data['body'] is None

def test_delete_return_404_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_task: Final = create_task(client, response_user['token'])

    response_delete: Final = client.delete(
        f"/api/v1/task/{55545456567}",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_delete.status_code == 404

    response_post_data: Final[Dict] = response_delete.json()

    assert response_post_data['code'] == 404
    assert response_post_data['message'] == "Task not found"
    assert response_post_data['status'] == False
    assert response_post_data['body'] is None

def test_return_bad_request_delete_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_delete: Final = client.delete(
        f"/api/v1/task/{0}",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_delete.status_code == 400

    response_post_data: Final[Dict] = response_delete.json()

    assert response_post_data['code'] == 400
    assert response_post_data['message'] == "Task Id is required"
    assert response_post_data['status'] == False
    assert response_post_data['body'] is None

def test_change_status_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_task: Final = create_task(client, response_user['token'])

    response_put: Final = client.put(
        f"/api/v1/task/{response_task['body']['id']}/toggle/status/is_done",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_put.status_code == 200

    response_post_data: Final[Dict] = response_put.json()

    assert response_post_data['code'] == 200
    assert response_post_data['message'] == "Task status changed with successfully"
    assert response_post_data['status'] == True
    assert response_post_data['body'] is not None

def test_put_return_404_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_task: Final = create_task(client, response_user['token'])

    response_put: Final = client.put(
        f"/api/v1/task/{55545456567}/toggle/status/is_done",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_put.status_code == 404

    response_post_data: Final[Dict] = response_put.json()

    assert response_post_data['code'] == 404
    assert response_post_data['message'] == "Task not found"
    assert response_post_data['status'] == False
    assert response_post_data['body'] is None

def test_return_bad_request_put_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_put: Final = client.put(
        f"/api/v1/task/{0}/toggle/status/is_done",
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_put.status_code == 400

    response_post_data: Final[Dict] = response_put.json()

    assert response_post_data['code'] == 400
    assert response_post_data['message'] == "Task Id is required"
    assert response_post_data['status'] == False
    assert response_post_data['body'] is None

def test_update_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_task: Final = create_task(client, response_user['token'])

    dto: Final[UpdateTaskDTO] = UpdateTaskDTO(
        title = "task updated",
        description= "task updated",
        is_done = True,
        due_date = None,
        priority = 6,
    )

    response_put: Final = client.put(
        f"/api/v1/task/{response_task['body']['id']}",
        headers={"Authorization": f"Bearer {response_user['token']}"},
        json=dto.model_dump()
    )

    if response_put.status_code != 200:
        print("Resposta do servidor:", response_put.json())
        print("Status Code:", response_put.status_code)

    assert response_put.status_code == 200

    response_post_data: Final[Dict] = response_put.json()

    assert response_post_data['code'] == 200
    assert response_post_data['message'] == "Task updated with successfully"
    assert response_post_data['status'] == True
    assert response_post_data['body']['title'] == dto.title
    assert response_post_data['body']['description'] == dto.description
    assert response_post_data['body']['priority'] == dto.priority
    
def test_put_return_404_update_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    response_task: Final = create_task(client, response_user['token'])

    dto: Final[UpdateTaskDTO] = UpdateTaskDTO(
        title = "task updated",
        description= "task updated",
        is_done = None,
        due_date = None,
        priority = 6,
    )

    response_put: Final = client.put(
        f"/api/v1/task/{55545456567}",
        json=dict(dto),
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_put.status_code == 404

    response_post_data: Final[Dict] = response_put.json()

    assert response_post_data['code'] == 404
    assert response_post_data['message'] == "Task not found"
    assert response_post_data['status'] == False
    assert response_post_data['body'] is None

def test_return_bad_request_update_task(client: TestClient):
    response_user: Final = create_user_return_token(client)

    dto: Final[UpdateTaskDTO] = UpdateTaskDTO(
        title = "task updated",
        description= "task updated",
        is_done = None,
        due_date = None,
        priority = 6,
    )

    response_put: Final = client.put(
        f"/api/v1/task/{0}",
        json=dict(dto),
        headers={"Authorization": f"Bearer {response_user['token']}"},
    )

    assert response_put.status_code == 400

    response_post_data: Final[Dict] = response_put.json()

    assert response_post_data['code'] == 400
    assert response_post_data['message'] == "Task Id is required"
    assert response_post_data['status'] == False
    assert response_post_data['body'] is None
