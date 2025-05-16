from pydantic import BaseModel, Field
from datetime import date

from src.production_monitor.models import ShiftTask


class ShiftTaskFilterParams(BaseModel):
    is_closed: bool | None = Field(
        default=None, description="Фильтр по статусу закрытия"
    )
    batch_number: int | None = Field(
        default=None, description="Фильтр по номеру партии"
    )
    batch_date: date | None = Field(default=None, description="Фильтр по дате партии")
    offset: int = Field(default=0, ge=0, description="Смещение")
    limit: int = Field(default=100, ge=1, le=1000, description="Лимит записей")


def build_shift_task_filters(
    is_closed: bool | None = None,
    batch_number: int | None = None,
    batch_date: date | None = None,
) -> list:
    filters = []
    if is_closed is not None:
        filters.append(ShiftTask.is_closed == is_closed)
    if batch_number is not None:
        filters.append(ShiftTask.batch_number == batch_number)
    if batch_date is not None:
        filters.append(ShiftTask.batch_date == batch_date)
    return filters
