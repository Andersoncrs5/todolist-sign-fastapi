from pydantic import BaseModel
from typing import TypeVar, Generic
from datetime import datetime

T = TypeVar('T')

class ResponseBody(BaseModel, Generic[T]):
    code: int
    message: str
    body: T
    status: bool
    datetime: str