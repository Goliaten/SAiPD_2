from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.app.schemas.example import DynamicMapData
from src.app.database import crud
from src.app.database.session import get_db

router = APIRouter(prefix="/dynamic_data")


@router.get(
    "/range/{shard_id}",
    response_model=List[DynamicMapData],
    tags=["dynamic_data"],
)
async def read_range_of_dynamic_war_data(
    shard_id: int,
    datetime_from: datetime,
    datetime_to: datetime,
    war_number: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    Endpoint not implemented due to permormance concerns.
    """
    raise HTTPException(
        status_code=501,
        detail="Endpoint not implemented due to permormance concerns.",
    )


@router.get(
    "/range/{shard_id}/{hex_id}",
    response_model=List[DynamicMapData],
    tags=["dynamic_data"],
)
async def read_range_of_dynamic_war_data_for_hex(
    shard_id: int,
    datetime_from: datetime,
    datetime_to: datetime,
    hex_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    Returns the dynamic war data for specific hex and shard for a range of dates.
    """
    filters = {"shard_id": shard_id}
    if hex_id:
        filters["hex_id"] = hex_id

    if datetime_from >= datetime_to:
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime range. `from` should be smaller than `to`.",
        )

    dynamic_data = await crud.list_dynamic_map_data_REV(
        db,
        datetime_from=datetime_from,
        datetime_to=datetime_to,
        skip=skip,
        limit=limit,
        **filters,
    )
    if not dynamic_data:
        raise HTTPException(status_code=404, detail="Dynamic map dat not found.")
    return dynamic_data


@router.get(
    "/{shard_id}/{hex_id}",
    response_model=DynamicMapData,
    tags=["dynamic_data"],
)
async def read_current_dynamic_map_data_for_hex(
    shard_id: int, hex_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Returns current/latest dynamic map data for a hex on a specific shard.
    """
    filters = {"shard_id": shard_id, "hex_id": hex_id}

    dynamic_data = await crud.get_dynamic_map_data_latest(db, **filters)
    if dynamic_data is None:
        raise HTTPException(status_code=404, detail="Dynamic map data not found.")
    return dynamic_data


@router.get(
    "/{shard_id}",
    response_model=List[DynamicMapData],
    tags=["dynamic_data"],
)
async def read_map_war_report_all_hexes(
    shard_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Returns current/latest dynamic map data for all hexes on a specific shard.
    This can return 23k lines of formatted json. Be careful of overusing this endpoint.
    """
    filters = {"shard_id": shard_id}

    dynamic_data = await crud.list_dynamic_map_data_latest(db, **filters)
    if dynamic_data is None:
        raise HTTPException(status_code=404, detail="Dynamic map dat not found.")
    return dynamic_data
