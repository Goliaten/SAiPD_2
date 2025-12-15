from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

from src.app.schemas.User import User, InputUserData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/add",
    response_model=int,
)
async def add_user(
    data: InputUserData,
    db: AsyncSession = Depends(get_db),
):
    """
    Add a new user.
    If data is correct, returns it's id in database.
    If wrong, throws exception
    """
    user_data = data.model_dump()
    user_data["is_active"] = True
    await db.begin()
    try:
        user = await crud.upsert_t_user(
            db,
            user_data,
            key_fields=["id", "login"],
            strict_insert=True,
        )
        if not user:
            raise ValueError("User with given login already exists.")
        role = await crud.get_t_role(db=db, is_default_user_role=True)
        if not role:
            raise ValueError("Role ID not found in database.")
        await crud.upsert_t_user_role(
            db,
            data={"user_id": user.id, "role_id": role.id},
        )
        await db.commit()

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid data. {e}")
    except Exception as e:
        import traceback

        await db.rollback()

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server exception: {e}.")

    return user.id


@router.get("/list", response_model=List[User])
async def list_all_users(
    skip: int = 0,
    limit: int = 100,
    is_active: bool | None = None,
    class_id: int | None = None,
    role_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    List users with optional filters:
    - `is_active`: filter by activation state
    - `class_id`: only users assigned to this class
    - `role_id`: only users assigned this role
    """
    # Base filter by is_active if provided
    filters = {}
    if is_active is not None:
        filters["is_active"] = is_active

    # If no class/role filters, use generic list
    if class_id is None and role_id is None:
        return await crud.list_t_user(db=db, skip=skip, limit=limit, **filters)

    # Gather candidate user ids from class and/or role associations
    user_ids: set[int] = set()
    # If class filter provided, collect users in class
    if class_id is not None:
        user_classes = await crud.list_t_user_class(db=db, class_id=class_id)
        user_ids = {uc.user_id for uc in user_classes}

    # If role filter provided, collect users with role
    if role_id is not None:
        user_roles = await crud.list_t_user_role(db=db, role_id=role_id)
        role_user_ids = {ur.user_id for ur in user_roles}
        user_ids = (
            role_user_ids if not user_ids else user_ids.intersection(role_user_ids)
        )

    # If no matching users, return empty list
    if not user_ids:
        return []

    # Fetch users and apply is_active filter if necessary
    users = []
    for uid in sorted(list(user_ids))[skip : skip + limit]:
        u = await crud.get_t_user(db=db, id=uid, **({} if not filters else filters))
        if u:
            users.append(u)

    return users


@router.get("/get/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Return a single user by id.
    """
    user = await crud.get_t_user(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id={user_id} not found."
        )
    return user


@router.post("/update/{user_id}")
async def update_user_data(
    user_id: int,
    data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    """
    Update user fields. Allowed fields: `first_name`, `last_name`, `email`, `password`, `is_active`.
    Returns updated user id on success.
    """
    allowed = {"first_name", "last_name", "email", "password", "is_active"}
    update_data = {k: v for k, v in data.items() if k in allowed}
    if not update_data:
        raise HTTPException(status_code=400, detail="No updatable fields provided.")

    await db.begin()
    try:
        # ensure user exists
        user = await crud.get_t_user(db, id=user_id)
        if not user:
            await db.rollback()
            raise HTTPException(
                status_code=404, detail=f"User with id={user_id} not found."
            )

        update_data["id"] = user_id
        await crud.upsert_t_user(
            db, update_data, key_fields=["id"], strict_update=False
        )
        await db.commit()
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

    return {"id": user_id}


@router.post("/add_role/{user_id}")
async def add_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    """
    Assign a role to a user.
    Returns True if assigned, False if already assigned.
    """
    await db.begin()
    try:
        user = await crud.get_t_user(db, id=user_id)
        role = await crud.get_t_role(db, id=role_id)
        if not user:
            await db.rollback()
            raise HTTPException(
                status_code=404, detail=f"User with id={user_id} not found."
            )
        if not role:
            await db.rollback()
            raise HTTPException(
                status_code=404, detail=f"Role with id={role_id} not found."
            )

        ur = await crud.upsert_t_user_role(
            db, data={"user_id": user_id, "role_id": role_id}, strict_insert=True
        )
        await db.commit()
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Role already assigned. {e}")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

    return True if ur else False


@router.post("/remove_role/{user_id}")
async def remove_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    """
    Remove a role from a user. Also removes the user from any classes (per TODO).
    Returns True if removed, False otherwise.
    """
    await db.begin()
    try:
        user = await crud.get_t_user(db, id=user_id)
        role = await crud.get_t_role(db, id=role_id)
        if not user:
            await db.rollback()
            raise HTTPException(
                status_code=404, detail=f"User with id={user_id} not found."
            )
        if not role:
            await db.rollback()
            raise HTTPException(
                status_code=404, detail=f"Role with id={role_id} not found."
            )

        deleted = await crud.delete_t_user_role(db, user_id=user_id, role_id=role_id)

        await db.commit()
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

    return True if deleted else False


async def change_user_activity_status(
    user_id: int, status: bool, db: AsyncSession = Depends(get_db)
):
    """
    Change activity status of user.
    """
    await db.begin()
    try:
        user = await crud.get_t_user(db, id=user_id)
        if not user:
            await db.rollback()
            raise HTTPException(
                status_code=404, detail=f"User with id={user_id} not found."
            )
        if user.is_active == status:
            await db.rollback()
            return False  # Already in given state

        await crud.upsert_t_user(
            db,
            {"id": user_id, "is_active": status},
            key_fields=["id"],
            strict_update=True,
        )

        await db.commit()
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

    return True


@router.post("/deactivate/{user_id}")
async def deactivate_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deactivate a user by setting is_active to False.
    Returns True if deactivated, False if user not found or already inactive.
    """
    return await change_user_activity_status(user_id=user_id, status=False, db=db)


@router.post("/activate/{user_id}")
async def activate_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Activate a user by setting is_active to True.
    Returns True if activated, False if user not found or already inactive.
    """
    return await change_user_activity_status(user_id=user_id, status=True, db=db)
