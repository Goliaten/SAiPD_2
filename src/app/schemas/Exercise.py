from datetime import datetime
from pydantic import BaseModel


class InputExerciseData(BaseModel):
    """
    For validating user input
    """

    name: str
    description: str


class Exercise(InputExerciseData):
    """
    For validating server output
    """

    id: int
    created_date: datetime
    modified_date: datetime
