import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Type

from sqlalchemy import delete as sa_delete, insert as sa_insert
from sqlalchemy import select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession
# sqlalchemy.orm imports not needed here

from src.app.database.models import (
    REV,
    DynamicMapData,
    DynamicMapDataItem,
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


# DynamicMapData
async def get_dynamic_map_data(db: AsyncSession, **filters) -> Optional[DynamicMapData]:
    # TODO make different getter since this item has children
    return await _get_one(db, DynamicMapData, **filters)


async def get_dynamic_map_data_latest(
    db: AsyncSession, **filters
) -> Optional[DynamicMapData]:
    data: Optional[DynamicMapData] = await _get_one_last(
        db, model=DynamicMapData, **filters
    )
    if not data:
        return None
    data.mapItems = await _get_many(db, DynamicMapDataItem, DynamicMapData_id=data.id)
    return data


async def list_dynamic_map_data(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[DynamicMapData]:
    return await _get_many(db, DynamicMapData, skip=skip, limit=limit, **filters)


async def list_dynamic_map_data_latest(
    db: AsyncSession, **filters
) -> List[DynamicMapData]:
    data: List[DynamicMapData] = await _get_many_last_by_hex_id(
        db, DynamicMapData, **filters
    )
    tasks = [_get_many(db, DynamicMapDataItem, DynamicMapData_id=x.id) for x in data]
    items = await asyncio.gather(*tasks)
    for y, x in enumerate(data):
        x.mapItems = items[y]
    return data


async def list_dynamic_map_data_REV(
    db: AsyncSession,
    datetime_from: datetime,
    datetime_to: datetime,
    skip: int = 0,
    limit: int = 100,
    **filters,
) -> List[DynamicMapData]:
    filters |= {"DATE_RANGE": [datetime_from, datetime_to]}

    data = await _get_many_REV(db, DynamicMapData, skip=skip, limit=limit, **filters)
    tasks = [_get_many(db, DynamicMapDataItem, DynamicMapData_id=x.id) for x in data]
    items = await asyncio.gather(*tasks)
    for y, x in enumerate(data):
        x.mapItems = items[y]
    return data


async def upsert_dynamic_map_data(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> DynamicMapData:
    return await _upsert(
        db,
        DynamicMapData,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_dynamic_map_data(db: AsyncSession, **filters) -> int:
    return await _delete(db, DynamicMapData, **filters)


# DynamicMapDataItem
async def get_dynamic_map_data_item(
    db: AsyncSession, **filters
) -> Optional[DynamicMapDataItem]:
    return await _get_one(db, DynamicMapDataItem, **filters)


async def list_dynamic_map_data_items(
    db: AsyncSession, skip: int = 0, limit: int = 100, **filters
) -> List[DynamicMapDataItem]:
    return await _get_many(db, DynamicMapDataItem, skip=skip, limit=limit, **filters)


async def list_dynamic_map_data_items_REV(
    db: AsyncSession,
    datetime_from: datetime,
    datetime_to: datetime,
    skip: int = 0,
    limit: int = 100,
    **filters,
) -> List[DynamicMapDataItem]:
    filters |= {"DATE_RANGE": [datetime_from, datetime_to]}
    return await _get_many_REV(
        db, DynamicMapDataItem, skip=skip, limit=limit, **filters
    )


async def upsert_dynamic_map_data_item(
    db: AsyncSession,
    data: Dict[str, Any],
    key_fields: List[str] = ["id"],
    strict_insert: bool = False,
    strict_update: bool = False,
) -> DynamicMapDataItem:
    return await _upsert(
        db,
        DynamicMapDataItem,
        key_fields=key_fields,
        data=data,
        strict_insert=strict_insert,
        strict_update=strict_update,
    )


async def delete_dynamic_map_data_item(db: AsyncSession, **filters) -> int:
    return await _delete(db, DynamicMapDataItem, **filters)
