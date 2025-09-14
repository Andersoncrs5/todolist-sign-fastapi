from fastapi_filter.contrib.sqlalchemy import Filter
from api.models.entities.task_entity import TaskEntity

class TaskFilter(Filter):
    title__ilike: str | None = None
    is_done: bool | None = None
    priority__gte: int | None = None
    priority__lte: int | None = None

    class Constants(Filter.Constants):
        model = TaskEntity
