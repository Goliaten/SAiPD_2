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
    exercise_data["id"] = None
    await db.begin()
    try:
        exercise = await crud.upsert_t_exercise(
            db,
            exercise_data,
            key_fields=["id", "name"],
            strict_insert=True,
        )
        if not exercise:
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

    return exercise.id


@router.get("/list", response_model=List[Exercise])
async def list_exercises(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    db: AsyncSession = Depends(get_db),
):
    """
    List all exercises. Optional filter by name.
    Returns list of Exercises, if they exist.
    """
    if name:
        return await crud.list_t_exercise(db, skip=skip, limit=limit, name=name)
    else:
        return await crud.list_t_exercise(db, skip=skip, limit=limit)


@router.post("/update/{exercise_id}")
async def update_exercise(
    exercise_id: int, data: InputExerciseData, db: AsyncSession = Depends(get_db)
):
    """
    Update an exercise by ID.
    """
    await db.begin()
    try:
        exercise_data = data.model_dump()
        exercise_data["id"] = exercise_id
        exercise = await crud.upsert_t_exercise(
            db,
            exercise_data,
            key_fields=["id"],
            strict_update=True,
        )
        if not exercise:
            raise ValueError("Exercise not found or update failed.")
        await db.commit()
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid data. {e}")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

    return {"message": "Exercise updated successfully"}
