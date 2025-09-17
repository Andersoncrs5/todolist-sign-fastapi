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
        from_attributes = True

class CreateTaskDTO(BaseModel):
    title: str = Field(
        ...,
        min_length=4,
        max_length=50,
        description="The title field must be between 4 and 50 characters."
    )

    description: str | None = Field(
        None,
        max_length=150,
        description="The description field can have a maximum size of 150 characters."
    )

    is_done: bool = Field(
        False,
        description="The is_done field indicates if the task is completed."
    )

    due_date: date | None = Field(
        None,
        description="The due date for the task."
    )
    priority: int = Field(
        1, 
        ge=1,
        le=10,
        description="The priority field must be an integer between 1 and 10."
    )

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
    title: str | None = Field(
        None,
        min_length=4,
        max_length=50,
        description="The title field must be between 4 and 50 characters."
    )

    description: str | None = Field(
        None,
        max_length=150,
        description="The description field can have a maximum size of 150 characters."
    )

    is_done: bool | None = Field(
        None,
        description="The is_done field indicates if the task is completed."
    )

    due_date: date | None = Field(
        None,
        description="The due date for the task."
    )

    priority: int | None = Field(
        None,
        le=10,
        description="The priority field must be an integer between 1 and 10."
    )

    