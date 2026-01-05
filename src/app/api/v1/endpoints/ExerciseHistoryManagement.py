import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas import ExerciseHistory, InputExerciseHistoryData
from src.app.core.typed_dicts import history_status
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/history", tags=["history"])


@router.post("/generate/{class_id}", response_model=bool)
async def generate_exercise_history(class_id, db: AsyncSession = Depends(get_db)):
    await db.begin()

    class_ = await crud.get_t_class(db, id=class_id)
    if not class_:
        return HTTPException(
            status_code=404, detail=f"Class with id={class_id} not found in database."
        )

    class_exercises = await crud.list_t_class_exercise(db, class_id=class_.id)
    if not class_exercises:
        return HTTPException(
            status_code=404,
            detail=f"Class with id={class_id} doesn't have exercises assigned.",
        )

    try:
        for c_exercise in class_exercises:
            # time_of_exercise = datetime.datetime.strptime(
            #     c_exercise.time_of_exercise, "%H:%M:%S"
            # )
            date_from = datetime.datetime.strptime(
                str(class_.date_from), "%Y-%m-%d %H:%M:%S"
            )
            date_to = datetime.datetime.strptime(
                str(class_.date_to), "%Y-%m-%d %H:%M:%S"
            )
            date_: datetime.datetime = (
                datetime.datetime(
                    year=date_from.year, month=date_from.month, day=date_from.day
                )
                # datetime.datetime(class_.date_from)
                + datetime.timedelta(weeks=c_exercise.week_offset or 0)
                + datetime.timedelta(
                    hours=c_exercise.time_of_exercise.hour,
                    minutes=c_exercise.time_of_exercise.minute,
                )
            )
            while date_.isoweekday() % 7 + 1 != c_exercise.day_of_week:
                date_ += datetime.timedelta(days=1)
                if date_ - date_from > datetime.timedelta(weeks=55):
                    raise OverflowError("Loop exception")

            while date_ < date_to:
                data = {
                    "class_exercise_id": c_exercise.id,
                    "datetime_of_class": date_,
                    "teacher_id": c_exercise.teacher_id,
                    "status": history_status.upcoming.name
                    if date_ > datetime.datetime.now()
                    else history_status.not_started.name,
                }
                await crud.upsert_t_exercise_history(
                    db,
                    data,
                    key_fields=["class_exercise_id, datetime_of_class"],
                    strict_insert=True,
                )
                date_ += datetime.timedelta(weeks=c_exercise.week_interval)

        await db.commit()
    except Exception as e:
        import traceback

        await db.rollback()

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server exception: {e}.")

    return True


@router.get("/list", response_model=List[ExerciseHistory])
async def list_exercise_histories(
    skip: int = 0,
    limit: int = 100,
    class_exercise_id: Optional[int] = None,
    teacher_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    filters = {}
    if class_exercise_id:
        filters["class_exercise_id"] = class_exercise_id
    if teacher_id:
        filters["teacher_id"] = teacher_id
    if status:
        filters["status"] = status

    return await crud.list_t_exercise_history(db, skip=skip, limit=limit, **filters)


@router.post("/update/{exercise_history_id}", response_model=List[ExerciseHistory])
async def update_exercise_history(
    exercise_history_id: int,
    data: InputExerciseHistoryData,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an exercise history by ID.
    """
    raise HTTPException(status_code=501)
    if name:
        return await crud.list_t_exercise(db, skip=skip, limit=limit, name=name)
    else:
        return await crud.list_t_exercise(db, skip=skip, limit=limit)


@router.get("/get/{exercise_history_id}", response_model=List[ExerciseHistory])
async def get_exercise_history(
    exercose_history_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Return a single exercise history by id.
    """
    ex_hist = await crud.get_t_exercise_history(db, id=exercose_history_id)
    if not ex_hist:
        raise HTTPException(
            status_code=404, detail=f"Data with id={exercose_history_id} not found."
        )
    return ex_hist
