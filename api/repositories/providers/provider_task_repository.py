from api.repositories.base.base_task_repository import BaseTaskRepository
from sqlalchemy.orm import Session
from datetime import datetime
from api.models.entities.task_entity import TaskEntity
from utils.filters.task_filter import TaskFilter
from sqlalchemy import select

class TaskRepositoryProvider(BaseTaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> (TaskEntity | None):
        stmt = select(TaskEntity).where(TaskEntity.id == id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all_user_id_filtered(self, user_id: int, filters: TaskFilter) -> list[TaskEntity]: 
        stmt = select(TaskEntity).where(TaskEntity.user_id == user_id)
        stmt = filters.filter(stmt)

        results = self.db.execute(stmt).scalars().all()
        return list(results)
    
    def delete(self, task: TaskEntity):
        self.db.delete(task)
        self.db.commit()
        
    def create(self, task: TaskEntity) -> TaskEntity:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def save(self, task: TaskEntity) -> TaskEntity:
        self.db.commit()
        self.db.refresh(task)

        return task
