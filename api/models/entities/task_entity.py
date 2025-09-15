from datetime import datetime, date
from typing import Text
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.configs.db.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.models.entities.user_entity import UserEntity
class TaskEntity(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    priority: Mapped[int | None] = mapped_column(Integer, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="tasks")

    def to_task_out(self):
        from api.models.schemas.task_schemas import TaskOUT

        return TaskOUT(
            id = self.id,
            title = self.title,
            description = self.description,
            is_done = self.is_done,
            due_date = str(self.due_date),
            priority = self.priority,
            user_id = self.user_id,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
        )