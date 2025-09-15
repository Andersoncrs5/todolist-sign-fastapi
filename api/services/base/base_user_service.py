from abc import ABC, abstractmethod
from api.models.entities.user_entity import UserEntity
from api.models.schemas.user_schemas import UpdateUserDTO, CreateUserDTO

class BaseUserService(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> UserEntity | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity | None:
        pass

    @abstractmethod
    def set_refresh_token(self, refresh_token: str, user: UserEntity) -> UserEntity:
        pass
    
    @abstractmethod
    def delete(self, user: UserEntity):
        pass

    @abstractmethod
    def update(self, user: UserEntity, dto: UpdateUserDTO) -> UserEntity:
        pass

    @abstractmethod
    def create(self, dto: CreateUserDTO) -> UserEntity:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass
