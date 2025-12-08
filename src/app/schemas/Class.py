from datetime import datetime
from pydantic import BaseModel


class InputClassData(BaseModel):
    """
    For validating user input
    """

    date_from: datetime
    date_to: datetime
    name: str


class Class(InputClassData):
    """
    For validating server output
    """

    id: int
    created_date: datetime
    modified_date: datetime
    is_active: bool
