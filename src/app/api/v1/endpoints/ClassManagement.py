from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

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
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    List all classes.
    """
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
    class_id: int, exercise_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Adds exercise to class.
    Returns True if added relation. False if not inserted.
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
        exercise_class = await crud.upsert_t_class_exercise(
            db,
            data={"exercise_id": exercise_id, "class_id": class_id},
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
    Not implemented
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
