import uuid
from datetime import date
from typing import List, Optional
from sqlalchemy import (
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    String,
    Boolean,
    Integer,
    Date
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TestMeasurementGroup(Base):
    __test__ = False
    __tablename__ = "test_measurement_group"
    __table_args__ = (
        PrimaryKeyConstraint("id", "creation_date", name="pk_test_measurement_group"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    creation_user: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    updated_user: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, unique=True
    )

    creation_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    visibility: Mapped[str] = mapped_column(String, nullable=False)
    updated_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    usage_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_using_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    filter_values: Mapped[List["FilterValues"]] = relationship(
        back_populates="test_measurement_group",
        cascade="all, delete-orphan"
    )

    creation_user_obj: Mapped["User"] = relationship(
        "User",
        foreign_keys=[creation_user],
        uselist=False,
        back_populates="created_test_measurement_group"
    )
    updated_user_obj: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[updated_user],
        uselist=False,
        back_populates="updated_test_measurement_group"
    )

class FilterValues(Base):
    __test__ = False
    __tablename__ = "filter_values"
    __table_args__ = (
        PrimaryKeyConstraint("id", "creation_date", name="pk_filter_values"),
        ForeignKeyConstraint(
            ["test_measurement_group_id", "creation_date"],
            ["test_measurement_group.id", "test_measurement_group.creation_date"],
            ondelete="CASCADE",
            name="fk_filter_values_test_measurement_group",
        ),
        {"postgresql_partition_by": "RANGE (creation_date)"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    test_measurement_group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    creation_date: Mapped[date] = mapped_column(Date, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    test_measurement_group: Mapped["TestMeasurementGroup"] = relationship(
        back_populates="filter_values"
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstname: Mapped[str]
    lastname: Mapped[str]
    role: Mapped[str]
    email: Mapped[str]

    created_test_measurement_group: Mapped[Optional["TestMeasurementGroup"]] = relationship(
        "TestMeasurementGroup",
        foreign_keys="[TestMeasurementGroup.creation_user]",
        back_populates="creation_user_obj",
        uselist=False
    )
    updated_test_measurement_group: Mapped[Optional["TestMeasurementGroup"]] = relationship(
        "TestMeasurementGroup",
        foreign_keys="[TestMeasurementGroup.updated_user]",
        back_populates="updated_user_obj",
        uselist=False
    )