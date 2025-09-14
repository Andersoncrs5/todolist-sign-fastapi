from abc import ABC, abstractmethod
from api.models.entities.user_entity import UserEntity

class BaseUserRepository(ABC):
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> (UserEntity | None):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> (UserEntity | None):
        pass

    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def delete(self, user: UserEntity):
        pass
    
    @abstractmethod
    def update(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def save(self, user: UserEntity) -> UserEntity:
        pass