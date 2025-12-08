from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.app.schemas import Exercise, InputExerciseData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/exercise", tags=["exercise"])


@router.post("/add", response_model=int)
async def add_exercise(data: InputExerciseData, db: AsyncSession = Depends(get_db)):
    """
    Add exercise
    """
    exercise_data = data.model_dump()
    exercise_data["is_active"] = True
    exercise_data["id"] = None
    await db.begin()
    try:
        class_ = await crud.upsert_t_class(
            db,
            exercise_data,
            key_fields=["id", "name"],
            strict_insert=True,
        )
        if not class_:
            raise ValueError("Exercise with given parameters already exists.")
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


@router.get("/list", response_model=List[Exercise])
async def list_classes(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    List all exercises.
    Returns list of Exercises, if they exist.
    """
    return await crud.list_t_exercise(db, skip=skip, limit=limit)


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
