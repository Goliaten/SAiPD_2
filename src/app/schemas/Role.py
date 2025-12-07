from datetime import datetime
from pydantic import BaseModel


class Role(BaseModel):
    id: int
    name: str
    created_date: datetime
    modified_date: datetime
    is_active: bool
    is_default_user_role: bool
    # TODO finish User schema
