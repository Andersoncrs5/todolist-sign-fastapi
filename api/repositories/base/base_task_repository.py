from abc import ABC, abstractmethod
from api.models.entities.task_entity import TaskEntity
from api.utils.filters.task_filter import TaskFilter

class BaseTaskRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> TaskEntity | None:
        pass
    
    @abstractmethod
    def get_all_user_id_filtered(self, user_id: int, filters: TaskFilter) -> list[TaskEntity]: 
        pass

    @abstractmethod
    def delete(self, task: TaskEntity):
        pass

    @abstractmethod
    def save(self, task: TaskEntity) -> TaskEntity:
        pass

    @abstractmethod
    def create(self, task: TaskEntity) -> TaskEntity:
        pass