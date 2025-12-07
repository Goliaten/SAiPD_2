from typing import Type
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Float,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declarative_base


# Base class for our SQLAlchemy models
Base: Type = declarative_base()


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


# Models for bb.sql tables
class T_USER(Base):
    __tablename__ = "T_USER"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    login: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True)


class T_ROLE(Base):
    __tablename__ = "T_ROLE"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    created_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True)


class T_PERMISSION(Base):
    __tablename__ = "T_PERMISSION"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)


class T_ROLE_PERMISSION(Base):
    __tablename__ = "T_ROLE_PERMISSION"
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("T_ROLE.id"))
    permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("T_PERMISSION.id"))


class T_USER_ROLE(Base):
    __tablename__ = "T_USER_ROLE"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("T_USER.id"))
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("T_ROLE.id"))


class T_MESSAGE(Base):
    __tablename__ = "T_MESSAGE"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("T_USER.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(String(255), nullable=True)


class T_CLASS(Base):
    __tablename__ = "T_CLASS"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    date_from: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    date_to: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True)


class T_USER_CLASS(Base):
    __tablename__ = "T_USER_CLASS"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("T_USER.id"))
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("T_CLASS.id"))


class T_EXERCISE(Base):
    __tablename__ = "T_EXERCISE"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class T_CLASS_EXERCISE(Base):
    __tablename__ = "T_CLASS_EXERCISE"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("T_CLASS.id"))
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey("T_EXERCISE.id"))


class T_EXERCISE_HISTORY(Base):
    __tablename__ = "T_EXERCISE_HISTORY"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_exercise_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("T_CLASS_EXERCISE.id"), nullable=True
    )
    created_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    datetime_of_class: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    teacher_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("T_USER.id"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(255), nullable=True)


class T_ATTENDANCE(Base):
    __tablename__ = "T_ATTENDANCE"
    exercise_history_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("T_EXERCISE_HISTORY.id")
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("T_USER.id"))
    created_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=True)


class T_TODO(Base):
    __tablename__ = "T_TODO"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_history_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("T_EXERCISE_HISTORY.id"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("T_USER.id"), nullable=True
    )
    created_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    task_type: Mapped[str] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=True)


class T_MARK(Base):
    __tablename__ = "T_MARK"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_history_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("T_EXERCISE_HISTORY.id"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("T_USER.id"), nullable=True
    )
    created_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
