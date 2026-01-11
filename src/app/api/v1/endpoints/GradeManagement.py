from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.app.schemas.Mark import Mark, InputMarkData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/grade", tags=["grade"])


@router.post("/", response_model=Mark)
async def create_grade(
    payload: InputMarkData, db: AsyncSession = Depends(get_db)
) -> Mark:
    try:
        await db.begin()
        data = payload.dict()
        created = await crud.upsert_t_mark(db, data)
        await db.commit()
        if not created:
            raise HTTPException(status_code=500, detail="Failed to create grade")
        return created
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Mark])
async def list_grades(
    skip: int = 0,
    limit: int = 100,
    exercise_history_id: Optional[int] = None,
    user_id: Optional[int] = None,
    teacher_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        # basic filters supported by T_MARK table
        filters = {}
        if exercise_history_id is not None:
            filters["exercise_history_id"] = exercise_history_id
        if user_id is not None:
            filters["user_id"] = user_id

        marks = await crud.list_t_mark(db, skip=skip, limit=limit, **filters)

        # If teacher_id filter requested, filter client-side via exercise_history
        if teacher_id is not None:
            filtered = []
            for m in marks:
                if m.exercise_history_id is None:
                    continue
                eh = await crud.get_t_exercise_history(db, id=m.exercise_history_id)
                if eh and eh.teacher_id == teacher_id:
                    filtered.append(m)
            return filtered

        return marks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=Mark)
async def get_grade(id: int, db: AsyncSession = Depends(get_db)) -> Mark:
    try:
        g = await crud.get_t_mark(db, id=id)
        if not g:
            raise HTTPException(status_code=404, detail="Grade not found")
        return g
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=Mark)
async def update_grade(
    id: int, payload: InputMarkData, db: AsyncSession = Depends(get_db)
) -> Mark:
    try:
        await db.begin()
        data = payload.dict()
        data["id"] = id
        updated = await crud.upsert_t_mark(db, data, strict_update=False)
        await db.commit()
        if not updated:
            raise HTTPException(status_code=404, detail="Grade not found")
        return updated
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}")
async def delete_grade(id: int, db: AsyncSession = Depends(get_db)):
    try:
        await db.begin()
        deleted = await crud.delete_t_mark(db, id=id)
        await db.commit()
        return {"deleted": deleted}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
