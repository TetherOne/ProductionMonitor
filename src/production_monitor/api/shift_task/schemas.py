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
