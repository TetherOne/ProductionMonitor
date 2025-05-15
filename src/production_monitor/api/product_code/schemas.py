from pydantic import BaseModel
from datetime import date


class ProductCodeCreateSchema(BaseModel):
    unique_code: str
    batch_number: int
    batch_date: date
