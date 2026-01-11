from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional

from src.app.schemas.Task import Task, InputTaskData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/", response_model=Task)
async def assign_task(
    payload: InputTaskData, db: AsyncSession = Depends(get_db)
) -> Task:
    """
    Create and assign a task to a student for a specific exercise.

    :param payload: Task data (exercise_history_id, user_id, task_type, title, content, status)
    :param db: Database session
    :return: Created task
    """
    try:
        await db.begin()

        # Verify exercise history exists
        ex_hist = await crud.get_t_exercise_history(db, id=payload.exercise_history_id)
        if not ex_hist:
            raise ValueError(
                f"Exercise history with id={payload.exercise_history_id} not found"
            )

        # Verify user (student) exists
        user = await crud.get_t_user(db, id=payload.user_id)
        if not user:
            raise ValueError(f"User with id={payload.user_id} not found")

        data = payload.dict()
        created = await crud.upsert_t_todo(db, data)
        await db.commit()

        if not created:
            raise HTTPException(status_code=500, detail="Failed to create task")
        return created
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=Sequence[Task])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    exercise_history_id: Optional[int] = None,
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> Sequence[Task]:
    """
    List tasks with optional filtering.

    :param skip: Pagination offset
    :param limit: Pagination limit
    :param exercise_history_id: Filter by exercise history ID
    :param user_id: Filter by user (student) ID
    :param status: Filter by task status (pending, in_progress, completed, to_redo, failed)
    :param db: Database session
    :return: List of tasks
    """
    try:
        filters = {}
        if exercise_history_id is not None:
            filters["exercise_history_id"] = exercise_history_id
        if user_id is not None:
            filters["user_id"] = user_id
        if status is not None:
            filters["status"] = status

        return await crud.list_t_todo(db, skip=skip, limit=limit, **filters)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=Task)
async def get_task(id: int, db: AsyncSession = Depends(get_db)) -> Task:
    """
    Retrieve a single task by ID.

    :param id: Task ID
    :param db: Database session
    :return: Task object
    """
    try:
        task = await crud.get_t_todo(db, id=id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=Task)
async def update_task(
    id: int, payload: InputTaskData, db: AsyncSession = Depends(get_db)
) -> Task:
    """
    Update a task by ID.

    :param id: Task ID
    :param payload: Updated task data
    :param db: Database session
    :return: Updated task
    """
    try:
        await db.begin()
        data = payload.dict()
        data["id"] = id
        updated = await crud.upsert_t_todo(db, data, strict_update=False)
        await db.commit()

        if not updated:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}/status/{new_status}")
async def update_task_status(
    id: int, new_status: str, db: AsyncSession = Depends(get_db)
):
    """
    Update task status (pending, in_progress, completed, to_redo, failed).

    :param id: Task ID
    :param new_status: New status for the task
    :param db: Database session
    :return: Updated task
    """
    try:
        await db.begin()

        # Get existing task
        task = await crud.get_t_todo(db, id=id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update status
        data = {
            "id": id,
            "status": new_status,
            "modified_date": datetime.now(),
        }
        updated = await crud.upsert_t_todo(
            db, data, key_fields=["id"], strict_update=False
        )
        await db.commit()

        return updated
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}")
async def delete_task(id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a task by ID.

    :param id: Task ID
    :param db: Database session
    :return: Count of deleted rows
    """
    try:
        await db.begin()
        deleted = await crud.delete_t_todo(db, id=id)
        await db.commit()

        if deleted == 0:
            raise HTTPException(status_code=404, detail="Task not found")

        return {"deleted": deleted}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
