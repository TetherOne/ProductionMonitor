from pydantic import BaseModel
from datetime import date, datetime


class ProductCodeBaseSchema(BaseModel):
    unique_code: str
    is_aggregated: bool
    aggregated_at: datetime | None
    shift_task_id: int


class ProductCodeSchema(ProductCodeBaseSchema):
    id: int


class ProductCodeCreateSchema(BaseModel):
    unique_code: str
    batch_number: int
    batch_date: date


class AggregateProductCodeRequest(BaseModel):
    shift_task_id: int
    unique_code: str


class AggregateProductCodeResponse(BaseModel):
    unique_code: str
