from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.production_monitor.api.product_code.schemas import (
    ProductCodeCreateSchema,
    AggregateProductCodeRequest,
)
from src.production_monitor.models import ShiftTask, ProductCode
from typing import Sequence

from src.production_monitor.utils.errors import NotFound, BadRequest


async def add_product_codes(
    session: AsyncSession,
    product_codes: Sequence[ProductCodeCreateSchema],
) -> Sequence[ProductCode]:
    result = []
    """
    Извлекает множество уникальных кодов, уже существующих в базе,
    из переданных на добавление к ShiftTask
    """
    existing_codes = {
        row[0]
        for row in await session.execute(
            select(ProductCode.unique_code).where(
                ProductCode.unique_code.in_([p.unique_code for p in product_codes])
            )
        )
    }

    for item in product_codes:
        if item.unique_code not in existing_codes:
            """
            Получаем соответствующую сменную задачу
            """
            shift_task = await session.scalar(
                select(ShiftTask).where(
                    ShiftTask.batch_number == item.batch_number,
                    ShiftTask.batch_date == item.batch_date,
                )
            )

            if shift_task:
                new_product = ProductCode(
                    unique_code=item.unique_code,
                    shift_task_id=shift_task.id,
                    is_aggregated=False,
                    aggregated_at=None,
                )
                result.append(new_product)
                session.add(new_product)

    await session.commit()
    return result


async def validate_product_codes(
    aggregate_product_codes: AggregateProductCodeRequest,
    session: AsyncSession,
) -> ProductCode:
    result = await session.execute(
        select(ProductCode).where(
            ProductCode.unique_code == aggregate_product_codes.unique_code,
        )
    )
    product_code = result.scalar_one_or_none()

    if product_code is None:
        raise NotFound("product code not found")

    if product_code.shift_task_id != aggregate_product_codes.shift_task_id:
        raise BadRequest("unique code is attached to another batch")

    if product_code.is_aggregated:
        raise BadRequest(
            f"unique code already used at {product_code.aggregated_at}",
        )

    return product_code
