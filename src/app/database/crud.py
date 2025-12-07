import asyncio
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Type

from sqlalchemy import delete as sa_delete, insert as sa_insert
from sqlalchemy import select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession
# sqlalchemy.orm imports not needed here

from src.app.database.models import (
    REV,
    T_USER,
    T_ROLE,
    T_PERMISSION,
    T_ROLE_PERMISSION,
    T_USER_ROLE,
    T_MESSAGE,
    T_CLASS,
    T_USER_CLASS,
    T_EXERCISE,
    T_CLASS_EXERCISE,
    T_EXERCISE_HISTORY,
    T_ATTENDANCE,
    T_TODO,
    T_MARK,
)


# Generic helpers
async def _get_one(db: AsyncSession, model: Type[Any], **filters) -> Optional[Any]:
    stmt = select(model).filter_by(**filters)
    result = await db.execute(stmt)
    return result.scalars().first()


# async def _get_one_last(db: AsyncSession, model: Type[Any], **filters) -> Optional[Any]:
async def _get_one_last(db: AsyncSession, model: Type[Any], **filters) -> Optional[Any]:
    stmt = select(model).filter_by(**filters).order_by(model.REV.desc())
    result = await db.execute(stmt)
    return result.scalars().first()


async def _get_many(
    db: AsyncSession, model: Type[Any], skip: int = 0, limit: int = 100, **filters
) -> List[Any]:
    stmt = select(model).filter_by(**filters).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def _get_many_last_by_hex_id(
    db: AsyncSession, model: Type[Any], skip: int = 0, limit: int = 100, **filters
) -> List[Any]:
    """
    For proper usage `hex_id` shouldn't be in filters.
    """
    stmt = (
        select(model)
        .filter_by(**filters)
        .order_by(model.REV.desc())
        .group_by(model.hex_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def _get_many_REV(
    db: AsyncSession, model: Type[Any], skip: int = 0, limit: int = 100, **filters
) -> List[Any]:
    """
    special filter key: DATE_RANGE. Should be a list of 2 ISO8601 compliant datetime strings. Will be used to filter by REV timestamp.
    """
    date_range = None
    if "DATE_RANGE" in filters:
        date_range = filters.pop("DATE_RANGE")
    else:
        raise ValueError("Date range missing.")

    stmt = (
        (
            select(model)
            .filter_by(**filters)
            .join(REV, model.REV == REV.REV)
            .where(
                REV.tmstmp.between(date_range[0].isoformat(), date_range[1].isoformat())
            )
        )
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def _delete(db: AsyncSession, model: Type[Any], **filters) -> int:
    stmt = sa_delete(model).filter_by(**filters)
    res = await db.execute(stmt)
    await db.commit()
    return res.rowcount if hasattr(res, "rowcount") else 0  # type: ignore


async def _upsert(
    db: AsyncSession,
    model: Type[Any],
    key_fields: Iterable[str],
    data: Dict[str, Any],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> Any:
    """
    Upsert helper: find by key_fields; update if exists, insert otherwise.
    If strict_insert is True, raise if record exists.
    If strict_update is True, raise if no record exists to update.
    """
    # Prefer updating by primary key if present in data and not null/None.
    pk_filters = {k: data[k] for k in key_fields if k in data and data[k] is not None}

    if pk_filters:
        existing = await _get_one(db, model, **pk_filters)

        if existing and strict_insert:
            raise ValueError("Record exists but strict_insert=True")

        if not existing and strict_update:
            raise ValueError("Record does not exist but strict_update=True")

        if existing:
            # update by PK
            await db.execute(
                sa_update(model)
                .where(*[getattr(model, k) == pk_filters[k] for k in pk_filters])
                .values(**data)
            )
            await db.commit()
            return await _get_one(db, model, **pk_filters)

        # If PK present but no existing and strict_update is False, insert
        stmt = sa_insert(model).values(**data)
        await db.execute(stmt)
        await db.commit()
        return await _get_one(db, model, **pk_filters)

    # No PK present: perform insert (do not attempt to match by other keys)
    if strict_update:
        # caller expected an update by PK but none was provided
        raise ValueError("strict_update=True but no primary key provided in data")

    # Insert
    stmt = sa_insert(model).values(**data)
    await db.execute(stmt)
    await db.commit()
    # Try to return by any provided key_fields if possible, otherwise return None
    return await _get_one(db, model, **{k: data[k] for k in data})


# Per-model CRUD wrappers


# --- CRUD for T_USER ---
async def get_t_user(db: AsyncSession, **filters) -> Optional[T_USER]:
    return await _get_one(db, T_USER, **filters)


async def list_t_user(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_USER]:
    return await _get_many(db, T_USER, skip=skip, limit=limit, **filters)


async def upsert_t_user(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_USER:
    return await _upsert(
        db,
        T_USER,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_user(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_USER, **filters)


# --- CRUD for T_ROLE ---
async def get_t_role(db: AsyncSession, **filters) -> Optional[T_ROLE]:
    return await _get_one(db, T_ROLE, **filters)


async def list_t_role(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_ROLE]:
    return await _get_many(db, T_ROLE, skip=skip, limit=limit, **filters)


async def upsert_t_role(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_ROLE:
    return await _upsert(
        db,
        T_ROLE,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_role(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_ROLE, **filters)


# --- CRUD for T_PERMISSION ---
async def get_t_permission(db: AsyncSession, **filters) -> Optional[T_PERMISSION]:
    return await _get_one(db, T_PERMISSION, **filters)


async def list_t_permission(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_PERMISSION]:
    return await _get_many(db, T_PERMISSION, skip=skip, limit=limit, **filters)


async def upsert_t_permission(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_PERMISSION:
    return await _upsert(
        db,
        T_PERMISSION,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_permission(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_PERMISSION, **filters)


# --- CRUD for T_ROLE_PERMISSION ---
async def get_t_role_permission(
    db: AsyncSession, **filters
) -> Optional[T_ROLE_PERMISSION]:
    return await _get_one(db, T_ROLE_PERMISSION, **filters)


async def list_t_role_permission(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_ROLE_PERMISSION]:
    return await _get_many(db, T_ROLE_PERMISSION, skip=skip, limit=limit, **filters)


async def upsert_t_role_permission(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["role_id", "permission_id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_ROLE_PERMISSION:
    return await _upsert(
        db,
        T_ROLE_PERMISSION,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_role_permission(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_ROLE_PERMISSION, **filters)


# --- CRUD for T_USER_ROLE ---
async def get_t_user_role(db: AsyncSession, **filters) -> Optional[T_USER_ROLE]:
    return await _get_one(db, T_USER_ROLE, **filters)


async def list_t_user_role(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_USER_ROLE]:
    return await _get_many(db, T_USER_ROLE, skip=skip, limit=limit, **filters)


async def upsert_t_user_role(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["user_id", "role_id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_USER_ROLE:
    return await _upsert(
        db,
        T_USER_ROLE,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_user_role(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_USER_ROLE, **filters)


# --- CRUD for T_MESSAGE ---
async def get_t_message(db: AsyncSession, **filters) -> Optional[T_MESSAGE]:
    return await _get_one(db, T_MESSAGE, **filters)


async def list_t_message(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_MESSAGE]:
    return await _get_many(db, T_MESSAGE, skip=skip, limit=limit, **filters)


async def upsert_t_message(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_MESSAGE:
    return await _upsert(
        db,
        T_MESSAGE,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_message(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_MESSAGE, **filters)


# --- CRUD for T_CLASS ---
async def get_t_class(db: AsyncSession, **filters) -> Optional[T_CLASS]:
    return await _get_one(db, T_CLASS, **filters)


async def list_t_class(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_CLASS]:
    return await _get_many(db, T_CLASS, skip=skip, limit=limit, **filters)


async def upsert_t_class(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_CLASS:
    return await _upsert(
        db,
        T_CLASS,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_class(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_CLASS, **filters)


# --- CRUD for T_USER_CLASS ---
async def get_t_user_class(db: AsyncSession, **filters) -> Optional[T_USER_CLASS]:
    return await _get_one(db, T_USER_CLASS, **filters)


async def list_t_user_class(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_USER_CLASS]:
    return await _get_many(db, T_USER_CLASS, skip=skip, limit=limit, **filters)


async def upsert_t_user_class(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["user_id", "class_id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_USER_CLASS:
    return await _upsert(
        db,
        T_USER_CLASS,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_user_class(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_USER_CLASS, **filters)


# --- CRUD for T_EXERCISE ---
async def get_t_exercise(db: AsyncSession, **filters) -> Optional[T_EXERCISE]:
    return await _get_one(db, T_EXERCISE, **filters)


async def list_t_exercise(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_EXERCISE]:
    return await _get_many(db, T_EXERCISE, skip=skip, limit=limit, **filters)


async def upsert_t_exercise(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_EXERCISE:
    return await _upsert(
        db,
        T_EXERCISE,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_exercise(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_EXERCISE, **filters)


# --- CRUD for T_CLASS_EXERCISE ---
async def get_t_class_exercise(
    db: AsyncSession, **filters
) -> Optional[T_CLASS_EXERCISE]:
    return await _get_one(db, T_CLASS_EXERCISE, **filters)


async def list_t_class_exercise(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_CLASS_EXERCISE]:
    return await _get_many(db, T_CLASS_EXERCISE, skip=skip, limit=limit, **filters)


async def upsert_t_class_exercise(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_CLASS_EXERCISE:
    return await _upsert(
        db,
        T_CLASS_EXERCISE,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_class_exercise(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_CLASS_EXERCISE, **filters)


# --- CRUD for T_EXERCISE_HISTORY ---
async def get_t_exercise_history(
    db: AsyncSession, **filters
) -> Optional[T_EXERCISE_HISTORY]:
    return await _get_one(db, T_EXERCISE_HISTORY, **filters)


async def list_t_exercise_history(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_EXERCISE_HISTORY]:
    return await _get_many(db, T_EXERCISE_HISTORY, skip=skip, limit=limit, **filters)


async def upsert_t_exercise_history(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_EXERCISE_HISTORY:
    return await _upsert(
        db,
        T_EXERCISE_HISTORY,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_exercise_history(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_EXERCISE_HISTORY, **filters)


# --- CRUD for T_ATTENDANCE ---
async def get_t_attendance(db: AsyncSession, **filters) -> Optional[T_ATTENDANCE]:
    return await _get_one(db, T_ATTENDANCE, **filters)


async def list_t_attendance(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_ATTENDANCE]:
    return await _get_many(db, T_ATTENDANCE, skip=skip, limit=limit, **filters)


async def upsert_t_attendance(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["exercise_history_id", "user_id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_ATTENDANCE:
    return await _upsert(
        db,
        T_ATTENDANCE,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_attendance(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_ATTENDANCE, **filters)


# --- CRUD for T_TODO ---
async def get_t_todo(db: AsyncSession, **filters) -> Optional[T_TODO]:
    return await _get_one(db, T_TODO, **filters)


async def list_t_todo(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_TODO]:
    return await _get_many(db, T_TODO, skip=skip, limit=limit, **filters)


async def upsert_t_todo(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_TODO:
    return await _upsert(
        db,
        T_TODO,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_todo(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_TODO, **filters)


# --- CRUD for T_MARK ---
async def get_t_mark(db: AsyncSession, **filters) -> Optional[T_MARK]:
    return await _get_one(db, T_MARK, **filters)


async def list_t_mark(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[T_MARK]:
    return await _get_many(db, T_MARK, skip=skip, limit=limit, **filters)


async def upsert_t_mark(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> T_MARK:
    return await _upsert(
        db,
        T_MARK,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_t_mark(db: AsyncSession, **filters) -> int:
    return await _delete(db, T_MARK, **filters)
