from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InputMessageData(BaseModel):
    """
    For validating user input
    """

    user_id: int
    sender_id: int
    title: str
    content: str


class Message(InputMessageData):
    """
    For validating server output
    """

    id: int
