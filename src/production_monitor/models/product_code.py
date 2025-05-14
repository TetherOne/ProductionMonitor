from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.production_monitor.models import Base
from src.production_monitor.models.mixins.id_int_pk import IdIntPkMixin


if TYPE_CHECKING:
    from src.production_monitor.models.shift_task import ShiftTask


class ProductCode(Base, IdIntPkMixin):
    unique_code: Mapped[str] = mapped_column(unique=True, index=True)
    is_aggregated: Mapped[bool] = mapped_column(default=False)
    aggregated_at: Mapped[datetime | None] = mapped_column(nullable=True)

    shift_task_id: Mapped[int] = mapped_column(ForeignKey("shift_tasks.id"))
    shift_task: Mapped["ShiftTask"] = relationship(back_populates="product_codes")
