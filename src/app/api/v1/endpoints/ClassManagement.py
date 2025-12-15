import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.app.schemas.Class import Class, InputClassData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/class", tags=["class"])


@router.post("/add", response_model=int)
async def add_class(data: InputClassData, db: AsyncSession = Depends(get_db)):
    """
    Endpoint for adding Class (a group for a semester, which holds all students).
    Returns id of the Class.
    """
    class_data = data.model_dump()
    # basic validation: date_from must be before date_to
    if class_data["date_from"] >= class_data["date_to"]:
        raise HTTPException(status_code=400, detail="date_from must be before date_to")

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


@router.get("/list", response_model=List[Class])
async def list_classes(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    date_from: Optional[datetime.datetime] = None,
    date_to: Optional[datetime.datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    List classes. Optional filters: `name`, `date_from`, `date_to`.
    Date filters will return classes that overlap the provided range if both are provided.
    """
    # simple equality filter for name
    if name:
        candidates = await crud.list_t_class(db, skip=skip, limit=limit, name=name)
    else:
        candidates = await crud.list_t_class(db, skip=skip, limit=limit)

    # filter by date range overlap if provided
    if date_from or date_to:
        df = date_from or datetime.datetime.min
        dt = date_to or datetime.datetime.max
        filtered = [c for c in candidates if c.date_from <= dt and c.date_to >= df]
        return filtered[skip : skip + limit]

    return candidates[skip : skip + limit]


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


@router.post("/add_user/{class_id}", response_model=bool, tags=["user"])
async def add_user_to_class(
    class_id: str, user_id: str, db: AsyncSession = Depends(get_db)
):
    """
    Adds user to class.
    Returns True if added relation. False if not inserted.
    """
    await db.begin()
    # check if class exists
    class_ = await crud.get_t_class(db, id=class_id)
    # check if user exists
    user = await crud.get_t_user(db, id=user_id)

    if not class_:
        raise HTTPException(
            status_code=400, detail=f"Class with id={class_id} does not exist."
        )
    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with id={user_id} does not exist."
        )

    try:
        user_class = await crud.upsert_t_user_class(
            db, data={"user_id": user_id, "class_id": class_id}, strict_insert=True
        )
        await db.commit()
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"User is already in this class. <{e}>"
        )

    if not user_class:
        return False
    return True


@router.post("/remove_user/{class_id}", response_model=bool, tags=["user"])
async def remove_user_from_class(
    class_id: int, user_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Remove user from class.
    Returns True if entry was removed.
    Returns False if entry wasn't removed due to not existing or failed deletion.
    """
    await db.begin()
    # check if class exists
    class_ = await crud.get_t_class(db, id=class_id)
    # check if user exists
    user = await crud.get_t_user(db, id=user_id)

    if not class_:
        raise HTTPException(
            status_code=400, detail=f"Class with id={class_id} does not exist."
        )
    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with id={user_id} does not exist."
        )

    try:
        user_class = await crud.delete_t_user_class(
            db, user_id=user_id, class_id=class_id
        )
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error: <{e}>")

    if not user_class:
        return False
    return True


@router.post("/add_exercise/{class_id}", response_model=bool, tags=["exercise"])
async def add_exercise_to_class(
    class_id: int,
    exercise_id: int,
    teacher_id: int,
    day_of_week: int,
    time_of_exercise: datetime.time,
    week_interval: Optional[int] = None,
    week_offset: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Adds exercise to class.
    Returns True if added relation. False if not inserted.

    :param class_id: ID of Class
    :type class_id: int
    :param exercise_id: ID of Exercise
    :type exercise_id: int
    :param teacher_id: ID of teacher assigned to this exercise by default
    :type teacher_id: int
    :param day_of_week: Day of week, that this exercise will be help for given class
    :type day_of_week: int
    :param time_of_exercise: At what time the exercise will be held
    :type time_of_exercise: datetime.time
    :param week_interval: How often this exercise should be held.
    :type week_interval: int
    :param week_offset: With 0, the exercise's instance will be set to begin with first available date in classes date range.
        By offsetting, the initial instance can be offset, which will also offset subsequent instances
    :type week_offset: int
    """
    await db.begin()
    # check if class exists
    class_ = await crud.get_t_class(db, id=class_id)
    # check if user exists
    exercise = await crud.get_t_exercise(db, id=exercise_id)

    if not class_:
        raise HTTPException(
            status_code=400, detail=f"Class with id={class_id} does not exist."
        )
    if not exercise:
        raise HTTPException(
            status_code=400, detail=f"User with id={exercise_id} does not exist."
        )

    try:
        data = {
            "exercise_id": exercise_id,
            "class_id": class_id,
            "teacher_id": teacher_id,
            "day_of_week": day_of_week,
            "time_of_exercise": time_of_exercise,
            "week_interval": week_interval,
            "week_offset": week_offset,
        }
        for key, value in data.copy().items():
            if not value:
                data.pop(key)

        exercise_class = await crud.upsert_t_class_exercise(
            db,
            data=data,
            key_fields=["class_id", "exercise_id"],
            strict_insert=True,
        )
        await db.commit()
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Exercise is already assigned to this class. <{e}>"
        )

    if not exercise_class:
        return False
    return True


@router.post("/remove_exercise/{class_id}", response_model=bool, tags=["exercise"])
async def remove_exercise_from_class(
    class_id: int, exercise_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Unassign exercise from class.
    """
    await db.begin()
    # check if class exists
    class_ = await crud.get_t_class(db, id=class_id)
    # check if user exists
    exercise = await crud.get_t_exercise(db, id=exercise_id)

    if not class_:
        raise HTTPException(
            status_code=400, detail=f"Class with id={class_id} does not exist."
        )
    if not exercise:
        raise HTTPException(
            status_code=400, detail=f"Exercise with id={exercise_id} does not exist."
        )

    try:
        user_class = await crud.delete_t_class_exercise(
            db, user_id=exercise_id, class_id=class_id
        )
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error: <{e}>")

    if not user_class:
        return False
    return True
