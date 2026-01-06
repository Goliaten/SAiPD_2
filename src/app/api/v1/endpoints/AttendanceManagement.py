import datetime
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas import Attendance
from src.app.core.enums import attendance_status
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/attend", tags=["attend"])


@router.get("/{exercise_history_id}/generate", response_model=int)
async def generate_attendance_list(
    exercise_history_id: int,
    force: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    Generates attendance for users that should be at specific exercise.

    Returns number of upserted rows.

    :param exercise_history_id: ID of exercise history item
    :type exercise_history_id: int
    :param force: Force recreation of all attendance for given exercise history
    :type force: bool
    """
    await db.begin()
    ex_hist = await crud.get_t_exercise_history(db, id=exercise_history_id)
    if not ex_hist:
        raise HTTPException(
            status_code=404, detail="No exercise history with given ID exists."
        )

    class_ex = await crud.get_t_class_exercise(db, id=ex_hist.class_exercise_id)
    if not class_ex:
        logger.logger.debug(class_ex.__dict__)
        raise HTTPException(
            status_code=500,
            detail="No class exercise found for given exercise history.",
        )

    # FIXME hardcoded user_class limit to 1000
    user_class = await crud.list_t_user_class(
        db, limit=1000, class_id=class_ex.class_id
    )
    if not user_class:
        raise HTTPException(
            status_code=400,
            detail="Class has no users assigned to it.",
        )

    upserted = 0
    att: Any = None
    for user_id in (x.user_id for x in user_class):
        data = {
            "exercise_history_id": exercise_history_id,
            "user_id": user_id,
            "status": attendance_status.not_happened.value,
            "modified_date": datetime.datetime.now(),
        }
        if not force:
            try:
                att = await crud.upsert_t_attendance(
                    db,
                    data,
                    key_fields=["exercise_history_id", "user_id"],
                    strict_insert=True,
                )
            except ValueError as e:
                logger.logger.debug(f"Caught expected insert exception. {e}")
        else:
            att = await crud.upsert_t_attendance(
                db, data, key_fields=["exercise_history_id", "user_id"]
            )
        if att:
            upserted += 1
            att = None

    await db.commit()
    logger.logger.info(f"Upserted {upserted} attendance into database.")
    return upserted


@router.get("/list", response_model=List[Attendance])
async def list_attendance(
    skip: int = 0,
    limit: int = 100,
    exercise_history_id: Optional[int] = None,
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    filters = {}
    if exercise_history_id:
        filters["exercise_history_id"] = exercise_history_id
    if user_id:
        filters["user_id"] = user_id
    if status:
        filters["status"] = status

    return await crud.list_t_attendance(db, skip=skip, limit=limit, **filters)


@router.get("/{exercise_history_id}/{user_id}/present", response_model=bool)
async def set_status_present(
    exercise_history_id: int,
    user_id: int,
    force: bool = False,
    db: AsyncSession = Depends(get_db),
):
    return await set_status(
        status=attendance_status.present.value,
        exercise_history_id=exercise_history_id,
        user_id=user_id,
        force=force,
        db=db,
    )


@router.get("/{exercise_history_id}/{user_id}/absent", response_model=bool)
async def set_status_absent(
    exercise_history_id: int,
    user_id: int,
    force: bool = False,
    db: AsyncSession = Depends(get_db),
):
    return await set_status(
        status=attendance_status.absent.value,
        exercise_history_id=exercise_history_id,
        user_id=user_id,
        force=force,
        db=db,
    )


@router.get("/{exercise_history_id}/{user_id}/late", response_model=bool)
async def set_status_late(
    exercise_history_id: int,
    user_id: int,
    force: bool = False,
    db: AsyncSession = Depends(get_db),
):
    return await set_status(
        status=attendance_status.late.value,
        exercise_history_id=exercise_history_id,
        user_id=user_id,
        force=force,
        db=db,
    )


async def set_status(
    status: str,
    exercise_history_id: int,
    user_id: int,
    force: bool = False,
    db: AsyncSession = Depends(get_db),
):
    await db.begin()
    data = {
        "exercise_history_id": exercise_history_id,
        "user_id": user_id,
        "status": status,
        "modified_date": datetime.datetime.now(),
    }
    if not force:
        try:
            att = await crud.upsert_t_attendance(
                db,
                data,
                key_fields=["exercise_history_id", "user_id"],
                strict_update=True,
            )
        except ValueError as e:
            raise HTTPException(
                status_code=404,
                detail=f"Attendance for user not found for this exercise history. Generate it first with /generate endpoint. <{e}>",
            )
    else:
        await crud.upsert_t_attendance(
            db, data, key_fields=["exercise_history_id", "user_id"]
        )
    await db.commit()
    return True
