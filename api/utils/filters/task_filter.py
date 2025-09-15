from api.models.entities.task_entity import TaskEntity
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional
from datetime import date, datetime

class TaskFilter(Filter):
    title__ilike: Optional[str] = Field(None, description="Search by title (case-insensitive).")
    description__ilike: Optional[str] = Field(None, description="Search by description (case-insensitive).")
    is_done: Optional[bool] = Field(None, description="Filter by task status.")
    priority__gte: Optional[int] = Field(None, description="Filter by priority, greater than or equal to.")
    priority__lte: Optional[int] = Field(None, description="Filter by priority, less than or equal to.")
    
    created_at__gte: Optional[datetime] = Field(None, description="Filter by creation date, greater than or equal to.")
    created_at__lte: Optional[datetime] = Field(None, description="Filter by creation date, less than or equal to.")
    due_date__gte: Optional[date] = Field(None, description="Filter by due date, greater than or equal to.")
    due_date__lte: Optional[date] = Field(None, description="Filter by due date, less than or equal to.")

    class Constants(Filter.Constants):
        model = TaskEntity
