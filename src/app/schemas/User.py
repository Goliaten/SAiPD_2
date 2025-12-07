from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    created_date: datetime
    modified_date: datetime
    first_name: str
    last_name: str
    login: str
    email: str
    password: str
    is_active: bool
    # TODO finish User schema
