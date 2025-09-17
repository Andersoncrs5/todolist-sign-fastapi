import pytest
from unittest.mock import MagicMock
from api.models.entities.task_entity import TaskEntity
from api.services.providers.provider_task_service import TaskServiceProvider
from api.models.entities.user_entity import UserEntity
from api.models.schemas.task_schemas import CreateTaskDTO, UpdateTaskDTO
from datetime import datetime, date
from typing import Final
import copy

@pytest.fixture
def mock_task_repository():
    return MagicMock()

@pytest.fixture
def task_service(mock_task_repository):
    return TaskServiceProvider(mock_task_repository)

mock_user: Final[UserEntity] = UserEntity(
        id = 1,
        name = "username" ,
        email = "username@gmail.com" ,
        password = "username",
        refresh_token = "username",
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )

mock_task: Final[TaskEntity] = TaskEntity(
    id = 1,
    title = "task title",
    description = "task description",
    is_done = False,
    due_date = None,
    priority = 1,
    user_id = mock_user.id,
    created_at = datetime.now(),
    updated_at = datetime.now(),
)

@pytest.fixture
def mock_task_entity():
    return TaskEntity(
        id = 1,
        title = "task title",
        description = "task description",
        is_done = False,
        due_date = None,
        priority = 1,
        user_id = mock_user.id,
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )

def test_task_get_by_id(task_service, mock_task_repository):
    mock_task_repository.get_by_id.return_value = mock_task

    task = task_service.get_by_id(mock_task.id)

    assert task is not None
    assert task.id == mock_task.id

    mock_task_repository.get_by_id.assert_called_once_with(mock_task.id)

def test_task_return_null_get_by_id(task_service, mock_task_repository):
    mock_task_repository.get_by_id.return_value = None

    task = task_service.get_by_id(mock_task.id)

    assert task is None

    mock_task_repository.get_by_id.assert_called_once_with(mock_task.id)

def test_task_return_null_when_pass_id_zero(task_service, mock_task_repository):

    task = task_service.get_by_id(0)
    task_two = task_service.get_by_id(-2)

    assert task is None
    assert task_two is None

    assert mock_task_repository.get_by_id.call_count == 0

def test_delete_task(task_service, mock_task_repository):
    mock_task_repository.delete.return_value = None

    task_service.delete(mock_task)

    mock_task_repository.delete.assert_called_once_with(mock_task)

def test_create_task(task_service, mock_task_repository):
    mock_task_repository.create.return_value = mock_task

    dto: Final = CreateTaskDTO(
        title = mock_task.title,
        description = mock_task.description,
        is_done = mock_task.is_done,
        due_date = mock_task.due_date,
        priority = mock_task.priority,
    )

    result: Final[TaskEntity] = task_service.create(mock_user, dto)

    assert result.id == mock_task.id
    assert result.description == mock_task.description
    assert result.is_done == mock_task.is_done
    assert result.due_date == mock_task.due_date
    assert result.priority == mock_task.priority

    assert mock_task_repository.create.call_count == 1

def test_change_status_done(task_service, mock_task_repository):
    task_copied: Final[TaskEntity] = copy.copy(mock_task)
    task_copied.is_done = not mock_task.is_done

    mock_task_repository.save.return_value = mock_task

    task_changed: Final = task_service.change_status_done(task_copied)

    assert task_changed.id == mock_task.id
    assert task_changed.is_done == mock_task.is_done

    assert mock_task_repository.save.call_count == 1

def test_update_only_title_and_desc(task_service, mock_task_repository):
    
    dto: Final[UpdateTaskDTO] = UpdateTaskDTO(
        title = "task title updated",
        description = "task description updated",
        is_done = None,
        due_date = None,
        priority = None,
    )

    task_after_updated: Final[TaskEntity] = copy.copy(mock_task)
    task_after_updated.title = str(dto.title)
    task_after_updated.description = dto.description

    mock_task_repository.save.return_value = task_after_updated

    task_updated: Final[TaskEntity] = task_service.update(mock_task, dto)

    assert task_updated.title == dto.title
    assert task_updated.description == dto.description

    assert mock_task_repository.save.call_count == 1

def teaast_update_only_is_done_and_due_date_priority(task_service, mock_task_repository):
    
    dto: Final[UpdateTaskDTO] = UpdateTaskDTO(
        title = None,
        description = None,
        is_done = True,
        due_date = None,
        priority = 9,
    )

    task_after_updated: Final[TaskEntity] = copy.copy(mock_task)
    task_after_updated.title = str(dto.title)
    task_after_updated.description = dto.description

    mock_task_repository.save.return_value = task_after_updated

    task_updated: Final[TaskEntity] = task_service.update(mock_task, dto)

    assert task_updated.title == dto.title
    assert task_updated.description == dto.description
    assert task_updated.priority == dto.priority
    assert task_updated.is_done == dto.is_done

    assert mock_task_repository.save.call_count == 1