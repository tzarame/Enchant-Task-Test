from datetime import datetime

from pydantic import BaseModel
from enum import Enum


class TaskStatus(Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    CANCELED = 'canceled'
    FAILED = 'failed'
    OVERDUE = 'overdue'


class Task(BaseModel):
    name: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    due_date: datetime
    user_login: str
