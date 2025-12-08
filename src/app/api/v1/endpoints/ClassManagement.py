from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

from src.app.schemas.Class import Class, InputClassData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/class")


@router.post("/add", response_model=int)
async def add_class(data: InputClassData, db: AsyncSession = Depends(get_db)):
    """
    Endpoint for adding Class (a group for a semester, which holds all students).
    Returns id of the Class.
    """
    class_data = data.model_dump()
    class_data["is_active"] = True
    class_data["id"] = None
    await db.begin()
    try:
        class_ = await crud.upsert_t_class(
            db,
            class_data,
            key_fields=["id", "name"],
            # key_fields=["name", "date_from", "date_to"],
            strict_insert=True,
        )
        if not class_:
            raise ValueError("Class with given parameters already exists.")
        await db.commit()

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid data. {e}")
    except Exception as e:
        import traceback

        await db.rollback()

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server exception: {e}.")

    return class_.id


@router.post("/list", response_model=List[Class])
async def list_classes(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.list_t_class(db, skip=skip, limit=limit)


@router.post("/update/{class_id}")
async def update_class(db: AsyncSession = Depends(get_db)):
    """
    Not implemented
    """
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented.",
    )


@router.post("/remove/{class_id}")
async def remove_class(db: AsyncSession = Depends(get_db)):
    """
    Not implemented
    """
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented.",
    )


@router.post("/add_user/{class_id}")
async def add_user_to_class(db: AsyncSession = Depends(get_db)):
    """
    Not implemented
    """
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented.",
    )


@router.post("/remove_user/{class_id}")
async def remove_user_to_class(db: AsyncSession = Depends(get_db)):
    """
    Not implemented
    """
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented.",
    )
