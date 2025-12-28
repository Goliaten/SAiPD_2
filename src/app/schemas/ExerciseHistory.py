from datetime import datetime
from pydantic import BaseModel


class InputExerciseHistoryData(BaseModel):
    """
    For validating user input
    """

    datetime_of_class: datetime
    teacher_id: int
    status: str


class ExerciseHistory(InputExerciseHistoryData):
    """
    For validating server output
    """

    id: int
    class_exercise_id: int
    created_date: datetime
    modified_date: datetime
    datetime_of_class: datetime
    teacher_id: int
    status: str
