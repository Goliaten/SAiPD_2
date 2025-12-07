from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

from src.app.schemas.User import User, InputUserData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/user")


@router.post(
    "/add",
    response_model=int,
)
async def add_user(
    data: InputUserData,
    db: AsyncSession = Depends(get_db),
):
    """
    Add a new user.
    If data is correct, returns it's id in database.
    If wrong, throws exception
    """
    user_data = data.model_dump()
    user_data["is_active"] = True
    await db.begin()
    try:
        user = await crud.upsert_t_user(
            db,
            user_data,
            key_fields=["id", "login"],
            strict_insert=True,
        )
        if not user:
            raise ValueError("User with given login already exists.")
        role = await crud.get_t_role(db=db, is_default_user_role=True)
        await crud.upsert_t_user_role(
            db,
            data={"user_id": user.id, "role_id": role.id},
        )
        await db.commit()

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid data. {e}")
    except Exception as e:
        import traceback

        await db.rollback()

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server exception: {e}.")

    return user.id


@router.get("/get", response_model=List[User])
async def get_all_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.list_t_user(db=db, skip=skip, limit=limit)


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
