from datetime import datetime, date
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.production_monitor.models.base import Base
from src.production_monitor.models.mixins.id_int_pk import IdIntPkMixin


if TYPE_CHECKING:
    from src.production_monitor.models.product_code import ProductCode


class ShiftTask(Base, IdIntPkMixin):
    task_representation: Mapped[str]
    work_center: Mapped[str]
    shift: Mapped[str]
    brigade: Mapped[str]

    batch_number: Mapped[int]
    batch_date: Mapped[date]

    nomenclature: Mapped[str]
    code_ekn: Mapped[str]
    rc_identifier: Mapped[str]

    shift_start: Mapped[datetime]
    shift_end: Mapped[datetime]

    is_closed: Mapped[bool] = mapped_column(default=False)
    closed_at: Mapped[datetime | None]

    product_codes: Mapped[list["ProductCode"]] = relationship(
        back_populates="shift_task", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint(
            "batch_number",
            "batch_date",
            name="uq_batch_number_date",
        ),
    )
