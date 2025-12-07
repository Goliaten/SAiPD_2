from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional

from src.app.database.models import T_USER
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/user")


@router.post(
    "/add",
    response_model=int,
)
async def add_user(
    data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    """
    Add a new user.
    If data is correct, returns it's id in database.
    If wrong, throws exception
    """
    user_data = {x: data.get(x, None) for x in T_USER.__annotations__}
    try:
        user = await crud.upsert_t_user(
            db, user_data, key_fields=["id", "email", "password"], strict_insert=True
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid data.")
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise e

    return user.id


@router.get("/get/{user_id}", response_model=None)
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
