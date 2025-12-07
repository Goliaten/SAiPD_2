from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional

from src.app.schemas import User
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/user")


@router.post(
    "/add",
    response_model=None,
)
async def add_user(
    data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented.",
    )


@router.get("/get/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented.",
    )


@router.post("/update/{user_id}")
async def update_user_data(
    user_id: int,
    data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented.",
    )


@router.post("/add_role/{user_id}")
async def add_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented.",
    )


@router.post("/remove_role/{user_id}")
async def remove_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented.",
    )
