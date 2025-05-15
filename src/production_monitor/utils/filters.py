from pydantic import BaseModel, Field
from datetime import date


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
