from datetime import datetime
from pydantic import BaseModel


class InputUserData(BaseModel):
    """
    For validating user input
    """

    first_name: str
    last_name: str
    login: str
    email: str
    password: str


class User(InputUserData):
    """
    For validating server output
    """

    id: int
    created_date: datetime
    modified_date: datetime
    is_active: bool
    # TODO finish User schema
