from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InputTaskData(BaseModel):
    """
    For validating user input
    """

    exercise_history_id: int
    user_id: int
    task_type: str
    title: str
    content: str
    status: Optional[str] = "pending"


class Task(InputTaskData):
    """
    For validating server output
    """

    id: int
    created_date: datetime
    modified_date: datetime
