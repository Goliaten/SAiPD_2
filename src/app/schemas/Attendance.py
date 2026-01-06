from datetime import datetime
from pydantic import BaseModel


class InputAttendanceData(BaseModel):
    """
    For validating user input
    """

    status: str


class Attendance(InputAttendanceData):
    """
    For validating server output
    """

    exercise_history_id: int
    user_id: int
    created_date: datetime
    modified_date: datetime
