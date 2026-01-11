from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InputMarkData(BaseModel):
    """
    For validating user input
    """

    exercise_history_id: int
    user_id: int
    grade: Optional[str] = None


class Mark(InputMarkData):
    """
    For validating server output
    """

    id: int
    created_date: datetime
    modified_date: datetime
