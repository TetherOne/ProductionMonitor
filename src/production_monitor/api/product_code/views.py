from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.production_monitor.utils.db_helper import db_helper
from src.production_monitor.api.product_code import crud
from src.production_monitor.api.product_code.schemas import (
    ProductCodeCreateSchema,
    AggregateProductCodeResponse,
    AggregateProductCodeRequest,
    ProductCodeSchema,
)

router = APIRouter(tags=["Product Codes"])


@router.post(
    "/add/",
    response_model=list[ProductCodeSchema],
    status_code=status.HTTP_201_CREATED,
)
async def add_product_code(
    product_codes: list[ProductCodeCreateSchema],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.add_product_codes(
        session=session,
        product_codes=product_codes,
    )


@router.post(
    "/aggregate/",
    response_model=AggregateProductCodeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def aggregate_product_code(
    aggregate_product_codes: AggregateProductCodeRequest,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    product_code = await crud.validate_product_codes(
        aggregate_product_codes=aggregate_product_codes,
        session=session,
    )
    product_code.is_aggregated = True
    product_code.aggregated_at = datetime.now()
    await session.commit()
    return AggregateProductCodeResponse(
        unique_code=product_code.unique_code,
    )
