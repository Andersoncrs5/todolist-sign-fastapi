from api.services.base.base_user_service import BaseUserService
from sqlalchemy.orm import Session
from sqlalchemy import select
from api.models.entities.user_entity import UserEntity
from api.models.schemas.user_schemas import UpdateUserDTO, CreateUserDTO
from api.repositories.base.base_user_repository import BaseUserRepository
from api.services.providers.provider_crypto_service import *

class UserServiceProvider(BaseUserService):
    def __init__(self, repository: BaseUserRepository):
        self.repository = repository

    def get_by_id(self, id: int) -> UserEntity | None:
        if id is None or id <= 0:
            return None

        return self.repository.get_by_id(id)

    def get_by_email(self, email: str) -> UserEntity | None:
        if email is None or email == "":
            return None

        return self.repository.get_by_email(email)

    def exists_by_email(self, email: str) -> bool:
        return self.repository.exists_by_email(email)

    def delete(self, user: UserEntity):
        return self.repository.delete(user)

    def create(self, dto: CreateUserDTO) -> UserEntity:
        user_mapped = dto.to_user_entity()
        user_mapped.password = hash_password(user_mapped.password)

        user_created = self.repository.create(user_mapped)

        return user_created

    def set_refresh_token(self, refresh_token: str, user: UserEntity) -> UserEntity:
        
        user.refresh_token = refresh_token
        return self.repository.save(user)

    def update(self, user: UserEntity, dto: UpdateUserDTO) -> UserEntity:
        if dto.name != None :
            user.name = dto.name

        if dto.password != None :
            user.password = hash_password(dto.password)

        return self.repository.update(user)     
