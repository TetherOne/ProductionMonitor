from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.production_monitor.utils.db_helper import db_helper
from . import crud
from .schemas import ProductCodeCreateSchema

router = APIRouter(tags=["Product Codes"])


@router.post(
    "/add/",
    status_code=status.HTTP_201_CREATED,
)
async def add_product_codes(
    product_codes: list[ProductCodeCreateSchema],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.add_product_codes(
        session=session,
        product_data=product_codes,
    )
