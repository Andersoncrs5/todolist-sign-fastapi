from abc import ABC, abstractmethod
from api.models.entities.task_entity import TaskEntity

class TaskService(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> (TaskEntity | None):
        pass

    @abstractmethod
    def delete(self, task: TaskEntity):
        pass