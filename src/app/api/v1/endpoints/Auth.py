from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "",
    response_model=int,
)
async def authenticate(
    login: str,
    passwd: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Check user credentials.
    Expects password hashed with MD5.
    """

    await db.begin()
    try:
        user = await crud.get_t_user(db, login=login, password=passwd)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials.")

        await db.commit()
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback

        await db.rollback()

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server exception: {e}.")

    return user.id
