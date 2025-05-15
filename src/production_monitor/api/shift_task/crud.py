from datetime import date

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.production_monitor.api.shift_task.schemas import ShiftTaskSchema
from src.production_monitor.models import ShiftTask


async def get_shift_tasks(
    session: AsyncSession,
    is_closed: bool | None = None,
    batch_number: int | None = None,
    batch_date: date | None = None,
    offset: int = 0,
    limit: int = 100,
) -> list[ShiftTaskSchema] | None:
    stmt = select(ShiftTask)
    filters = []
    if is_closed is not None:
        filters.append(ShiftTask.is_closed == is_closed)
    if batch_number is not None:
        filters.append(ShiftTask.batch_number == batch_number)
    if batch_date is not None:
        filters.append(ShiftTask.batch_date == batch_date)

    if filters:
        stmt = stmt.where(and_(*filters))

    stmt = stmt.offset(offset).limit(limit)

    result = await session.scalars(stmt)
    shift_tasks = result.all()
    return [ShiftTaskSchema.from_orm(task) for task in shift_tasks]


async def get_shift_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> ShiftTaskSchema | None:
    stmt = select(ShiftTask).where(ShiftTask.id == task_id)
    result = await session.scalar(stmt)
    return result
