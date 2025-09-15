from abc import ABC, abstractmethod
from api.models.entities.task_entity import TaskEntity
from api.models.entities.user_entity import UserEntity
from api.utils.filters.task_filter import TaskFilter
from typing import List
from api.models.schemas.task_schemas import UpdateTaskDTO, CreateTaskDTO

class BaseTaskService(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> (TaskEntity | None):
        pass

    @abstractmethod
    def delete(self, task: TaskEntity):
        pass

    @abstractmethod
    def create(self, user: UserEntity, dto: CreateTaskDTO) -> TaskEntity:
        pass

    @abstractmethod
    def update(self, task: TaskEntity, dto: UpdateTaskDTO) -> TaskEntity:
        pass

    @abstractmethod
    def get_all_user_id_filtered(self, user_id: int, filters: TaskFilter) -> List[TaskEntity]: 
        pass

    @abstractmethod
    def change_status_done(self, task: TaskEntity) -> TaskEntity:
        pass
    