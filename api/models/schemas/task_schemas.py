from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date

class TaskOUT(BaseModel):
    id: int
    title: str
    description: str | None
    is_done: bool
    due_date: date | None | str
    priority: int | None
    user_id: int
    created_at: str | datetime
    updated_at: str | datetime

    class Config:
        orm_mode = True

class CreateTaskDTO(BaseModel):
    title: str
    description: str | None
    is_done: bool
    due_date: date | None
    priority: int | None

    def to_task_entity(self):
        from api.models.entities.task_entity import TaskEntity

        return TaskEntity(
            title = self.title,
            description = self.description,
            is_done = self.is_done,
            due_date = self.due_date,
            priority = self.priority,
        )

class UpdateTaskDTO(BaseModel):
    title: str | None
    description: str | None
    is_done: bool | None
    due_date: date | None
    priority: int | None

    