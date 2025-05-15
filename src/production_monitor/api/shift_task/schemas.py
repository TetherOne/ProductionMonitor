from pydantic import BaseModel
from datetime import datetime, date


class ShiftTaskBaseSchema(BaseModel):
    task_representation: str
    work_center: str
    shift: str
    brigade: str

    batch_number: int
    batch_date: date

    nomenclature: str
    code_ekn: str
    rc_identifier: str

    shift_start: datetime
    shift_end: datetime

    is_closed: bool = False
    closed_at: datetime | None = None

    model_config = {"from_attributes": True}


class ShiftTaskSchema(ShiftTaskBaseSchema):
    id: int


class ShiftTaskCreateSchema(ShiftTaskBaseSchema):
    pass


class ShiftTaskUpdateSchema(BaseModel):
    task_representation: str | None = None
    work_center: str | None = None
    shift: str | None = None
    brigade: str | None = None

    batch_number: int | None = None
    batch_date: date | None = None

    nomenclature: str | None = None
    code_ekn: str | None = None
    rc_identifier: str | None = None

    shift_start: datetime | None = None
    shift_end: datetime | None = None
    is_closed: bool | None = None
