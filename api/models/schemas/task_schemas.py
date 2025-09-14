from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date

class TaskOUT(BaseModel):
    id: int
    title: str
    description: str
    is_done: bool
    due_date: date | None
    priority: int | None
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True