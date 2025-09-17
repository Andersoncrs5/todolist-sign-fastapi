import pytest
from unittest.mock import MagicMock
from api.services.providers.provider_user_service import UserServiceProvider
from api.models.entities.user_entity import UserEntity
from api.models.schemas.user_schemas import CreateUserDTO, UpdateUserDTO
from datetime import datetime
from typing import Final

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def mock_hash_password(monkeypatch):
    mock_func = MagicMock(return_value="hashed_password_from_mock")
    monkeypatch.setattr("api.services.providers.provider_user_service.hash_password", mock_func)
    return mock_func

@pytest.fixture
def user_service(mock_user_repository):
    return UserServiceProvider(repository=mock_user_repository)

mock_user: Final[UserEntity] = UserEntity(
        id = 1,
        name = "username" ,
        email = "username@gmail.com" ,
        password = "username",
        refresh_token = "username",
        created_at = datetime.now(),
        updated_at = datetime.now(),
    )

@pytest.fixture
def mock_user_entity():
    return UserEntity(
        id=1,
        name="Old Name",
        email="test@example.com",
        password="old_hash",
        refresh_token="some_token",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

def test_set_refresh_token(user_service, mock_user_repository):
    new_token = "new_refresh_token_123"

    mock_user_repository.save.return_value = mock_user

    updated_user = user_service.set_refresh_token(new_token, mock_user)

    assert updated_user.refresh_token == new_token
    assert updated_user.id == 1
    
    mock_user_repository.save.assert_called_once_with(mock_user)

def test_delete(user_service, mock_user_repository):
    mock_user_repository.delete.return_value = None

    user_service.delete(mock_user)

    mock_user_repository.delete.assert_called_once_with(mock_user)
    assert mock_user_repository.delete.call_count == 1

def test_exists_by_email_returns_true(user_service, mock_user_repository):
    mock_user_repository.exists_by_email.return_value = True

    email_to_check = "test@example.com"
    check = user_service.exists_by_email(email_to_check)

    assert check is True

    mock_user_repository.exists_by_email.assert_called_once_with(email_to_check)

def test_return_null_get_by_email(user_service, mock_user_repository):
    mock_user_repository.get_by_email.return_value = None

    user = user_service.get_by_email("")

    assert user is None

    assert mock_user_repository.get_by_email.call_count == 0

def test_get_by_email(user_service, mock_user_repository):
    mock_user_repository.get_by_email.return_value = mock_user

    user = user_service.get_by_email(mock_user.email)

    assert user is not None

    assert user.id == mock_user.id
    assert user.email == mock_user.email

    mock_user_repository.get_by_email.assert_called_once_with(user.email)

def test_get_by_id_with_valid_id(user_service, mock_user_repository):
    mock_user_repository.get_by_id.return_value = mock_user

    user = user_service.get_by_id(mock_user.id)

    assert user is not None
    assert user.id == mock_user.id
    assert user.email == mock_user.email

    mock_user_repository.get_by_id.assert_called_once_with(1)

def test_return_null_when_get_user_by_id(user_service, mock_user_repository):
    user = user_service.get_by_id(0)

    assert user is None

    mock_user_repository.get_by_id.assert_not_called()

def test_create_user(user_service, mock_user_repository):
    dto = CreateUserDTO(
        name = mock_user.name,
        email = mock_user.email,
        password = mock_user.password,
    )

    mock_user_repository.create.return_value = mock_user


    user_created = user_service.create(dto)

    assert user_created.id == mock_user.id
    assert user_created.name == mock_user.name
    assert user_created.email == mock_user.email

    mock_user_repository.create.assert_called_once()

def test_update_user_with_name_and_password(user_service, mock_user_repository, mock_hash_password, mock_user_entity):
    dto = UpdateUserDTO(name="New Name", password="new_password123")
    
    mock_user_repository.update.return_value = mock_user_entity
    
    updated_user = user_service.update(mock_user_entity, dto)
    
    assert updated_user.name == "New Name"
    assert updated_user.password == "hashed_password_from_mock"
    
    mock_hash_password.assert_called_once_with("new_password123")
    mock_user_repository.update.assert_called_once_with(updated_user)

def test_update_user_only_name(user_service, mock_user_repository, mock_hash_password, mock_user_entity):
    dto = UpdateUserDTO(name="New Name", password=None)
    
    mock_user_repository.update.return_value = mock_user_entity

    updated_user = user_service.update(mock_user_entity, dto)
    
    assert updated_user.name == "New Name"
    assert updated_user.password == "old_hash"
    
    mock_hash_password.assert_not_called()
    mock_user_repository.update.assert_called_once_with(updated_user)

def test_update_user_only_password(user_service, mock_user_repository, mock_hash_password, mock_user_entity):
    dto = UpdateUserDTO(name=None, password="new_password123")
    
    mock_user_repository.update.return_value = mock_user_entity
    
    updated_user = user_service.update(mock_user_entity, dto)
    
    assert updated_user.name == "Old Name"
    assert updated_user.password == "hashed_password_from_mock"
    
    mock_hash_password.assert_called_once_with("new_password123")
    mock_user_repository.update.assert_called_once_with(updated_user)

def test_update_user_with_no_changes(user_service, mock_user_repository, mock_hash_password, mock_user_entity):
    
    dto = UpdateUserDTO(name=None, password=None)
    
    mock_user_repository.update.return_value = mock_user_entity
    
    updated_user = user_service.update(mock_user_entity, dto)
    
    assert updated_user.name == "Old Name"
    assert updated_user.password == "old_hash"
    
    mock_hash_password.assert_not_called()
    mock_user_repository.update.assert_called_once_with(updated_user)