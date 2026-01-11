from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional

from src.app.schemas.Message import Message, InputMessageData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/msg", tags=["msg"])


@router.post("/", response_model=Message)
async def send_message(
    payload: InputMessageData, db: AsyncSession = Depends(get_db)
) -> Message:
    """
    Send a message from one user to another.

    :param payload: Message data (user_id, sender_id, title, content)
    :param db: Database session
    :return: Created message
    """
    try:
        await db.begin()

        # Verify sender exists
        sender = await crud.get_t_user(db, id=payload.sender_id)
        if not sender:
            raise ValueError(f"Sender with id={payload.sender_id} not found")

        # Verify recipient exists
        recipient = await crud.get_t_user(db, id=payload.user_id)
        if not recipient:
            raise ValueError(f"Recipient with id={payload.user_id} not found")

        data = payload.dict()
        created = await crud.upsert_t_message(db, data)
        await db.commit()

        if not created:
            raise HTTPException(status_code=500, detail="Failed to create message")
        return created
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=Sequence[Message])
async def list_messages(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    sender_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
) -> Sequence[Message]:
    """
    List messages with optional filtering.

    :param skip: Pagination offset
    :param limit: Pagination limit
    :param user_id: Filter by recipient user ID
    :param sender_id: Filter by sender user ID
    :param db: Database session
    :return: List of messages
    """
    try:
        filters = {}
        if user_id is not None:
            filters["user_id"] = user_id
        if sender_id is not None:
            filters["sender_id"] = sender_id

        return await crud.list_t_message(db, skip=skip, limit=limit, **filters)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=Message)
async def get_message(id: int, db: AsyncSession = Depends(get_db)) -> Message:
    """
    Retrieve a single message by ID.

    :param id: Message ID
    :param db: Database session
    :return: Message object
    """
    try:
        msg = await crud.get_t_message(db, id=id)
        if not msg:
            raise HTTPException(status_code=404, detail="Message not found")
        return msg
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}")
async def delete_message(id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a message by ID.

    :param id: Message ID
    :param db: Database session
    :return: Count of deleted rows
    """
    try:
        await db.begin()
        deleted = await crud.delete_t_message(db, id=id)
        await db.commit()

        if deleted == 0:
            raise HTTPException(status_code=404, detail="Message not found")

        return {"deleted": deleted}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
