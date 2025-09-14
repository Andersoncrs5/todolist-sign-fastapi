from abc import ABC, abstractmethod

class BaseUserRepository(ABC):
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

