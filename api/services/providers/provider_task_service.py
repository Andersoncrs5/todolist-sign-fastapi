from api.services.base.base_task_service import BaseTaskService
from api.models.entities.task_entity import TaskEntity
from api.models.entities.user_entity import UserEntity
from api.utils.filters.task_filter import TaskFilter
from typing import List, Final
from api.repositories.base.base_task_repository import BaseTaskRepository
from api.models.schemas.task_schemas import UpdateTaskDTO, CreateTaskDTO

class TaskServiceProvider(BaseTaskService):
    def __init__(self, repository: BaseTaskRepository):
        self.repository = repository

    def get_by_id(self, id: int) -> (TaskEntity | None):
        if id <= 0 or id is None:
            return None

        return self.repository.get_by_id(id)

    def get_all_user_id_filtered(self, user_id: int, filters: TaskFilter) -> list[TaskEntity]:
        return self.repository.get_all_user_id_filtered(user_id, filters)

    def delete(self, task: TaskEntity):
        self.repository.delete(task)
        
    def create(self, user: UserEntity, dto: CreateTaskDTO) -> TaskEntity:
        task_mapped: Final[TaskEntity] = dto.to_task_entity()
        task_mapped.user_id = user.id

        return self.repository.create(task_mapped)

    def update(self, task: TaskEntity, dto: UpdateTaskDTO) -> TaskEntity:
        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        return self.repository.save(task)
    
    def change_status_done(self, task: TaskEntity) -> TaskEntity:   
        task.is_done = not task.is_done

        return self.repository.save(task)