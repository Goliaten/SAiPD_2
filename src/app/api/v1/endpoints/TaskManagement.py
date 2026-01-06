import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.app.schemas.Class import Class, InputClassData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/task", tags=["task"])
