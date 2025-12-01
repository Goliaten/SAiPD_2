from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declarative_base


# Base class for our SQLAlchemy models
Base = declarative_base()


class REV(Base):
    __tablename__ = "REV"
    REV: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmstmp: Mapped[DateTime] = mapped_column(DateTime)


class DynamicMapData(Base):
    __tablename__ = "DynamicMapData"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    hex_id: Mapped[int] = mapped_column(Integer, ForeignKey("hex.id"))
    shard_id: Mapped[int] = mapped_column(Integer, ForeignKey("shard.id"))
    regionId: Mapped[int] = mapped_column(Integer, nullable=True)
    scorchedVictoryTowns: Mapped[int] = mapped_column(Integer, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=True)

    rev = relationship("REV")
    hex = relationship("Hex")
    shard = relationship("Shard")
    items = relationship(
        "DynamicMapDataItem", back_populates="dynamic_map", cascade="all, delete-orphan"
    )


class DynamicMapDataItem(Base):
    __tablename__ = "DynamicMapDataItem"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    REV: Mapped[int] = mapped_column(Integer, ForeignKey("REV.REV"))
    DynamicMapData_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("DynamicMapData.id")
    )
    teamId: Mapped[str] = mapped_column(String(20), nullable=True)
    iconType: Mapped[int] = mapped_column(
        Integer, ForeignKey("StructureTypes.id"), nullable=True
    )
    x: Mapped[float] = mapped_column(Float, nullable=True)
    y: Mapped[float] = mapped_column(Float, nullable=True)
    flags: Mapped[int] = mapped_column(Integer, nullable=True)
    viewDirection: Mapped[int] = mapped_column(Integer, nullable=True)

    rev = relationship("REV")
    dynamic_map = relationship("DynamicMapData", back_populates="items")
