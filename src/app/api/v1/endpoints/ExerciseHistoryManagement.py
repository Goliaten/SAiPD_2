import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.typed_dicts import history_status
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/history", tags=["history"])


@router.post("/generate/{class_id}", response_model=None)
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
            date_: datetime.datetime = (
                class_.date_from
                + datetime.timedelta(weeks=c_exercise.week_offset or 0)
                + c_exercise.time_of_exercise
            )
            while date_.isoweekday() % 7 + 1 != c_exercise.day_of_week:
                date_ += datetime.timedelta(days=1)
                if date_ - class_.date_from > datetime.timedelta(weeks=55):
                    raise OverflowError("Loop exception")

            while date_ < class_.date_to:
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
