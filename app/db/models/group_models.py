import uuid
from datetime import date
from typing import List, Optional
from sqlalchemy import (
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    String,
    Boolean,
    Integer,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

# Make sure your GroupVisibility is defined/imported correctly
# from your_module import GroupVisibility

class BaseModel(DeclarativeBase):
    pass


class TestMeasurementGroup(BaseModel):
    __test__ = False
    __tablename__ = "test_measurement_group"
    __table_args__ = (
        PrimaryKeyConstraint("id", "creation_date", name="pk_test_measurement_group"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    creation_user: Mapped[str] = mapped_column(String, nullable=False)
    creation_date: Mapped[date] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    visibility: Mapped["GroupVisibility"] = mapped_column(nullable=False)  # Handle GroupVisibility properly
    updated_user: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    updated_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    usage_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_using_date: Mapped[Optional[date]] = mapped_column(nullable=True)

    filter_values: Mapped[List["FilterValues"]] = relationship(
        back_populates="test_measurement_group",
        cascade="all, delete-orphan"
    )


class FilterValues(BaseModel):
    __test__ = False
    __tablename__ = "filter_values"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_filter_values"),
        ForeignKeyConstraint(
            ["test_measurement_group_id", "creation_date"],
            ["test_measurement_group.id", "test_measurement_group.creation_date"],
            ondelete="CASCADE",
            name="fk_filter_values_test_measurement_group",
        ),
        {"postgresql_partition_by": "RANGE (creation_date)"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    test_measurement_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    creation_date: Mapped[date] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    test_measurement_group: Mapped["TestMeasurementGroup"] = relationship(
        back_populates="filter_values"
    )
