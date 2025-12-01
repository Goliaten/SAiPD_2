from typing import List, Optional
from pydantic import BaseModel


class DynamicMapDataItem(BaseModel):
    id: int
    REV: int
    DynamicMapData_id: int
    teamId: Optional[str]
    iconType: Optional[int]
    x: Optional[float]
    y: Optional[float]
    flags: Optional[int]
    viewDirection: Optional[int]


class DynamicMapData(BaseModel):
    id: int
    REV: int
    hex_id: int
    shard_id: int
    regionId: int
    scorchedVictoryTowns: Optional[int]
    version: Optional[int]
    mapItems: List[DynamicMapDataItem]

    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
