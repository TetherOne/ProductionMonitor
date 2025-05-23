from datetime import date, datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.production_monitor.api.shift_task.schemas import (
    ShiftTaskSchema,
    ShiftTaskCreateSchema,
    ShiftTaskUpdateSchema,
)
from src.production_monitor.models import ShiftTask
from src.production_monitor.utils.filters import build_shift_task_filters


async def get_shift_tasks(
    session: AsyncSession,
    is_closed: bool | None = None,
    batch_number: int | None = None,
    batch_date: date | None = None,
    offset: int = 0,
    limit: int = 100,
) -> list[ShiftTaskSchema] | None:
    stmt = select(ShiftTask)
    filters = build_shift_task_filters(is_closed, batch_number, batch_date)
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


async def create_shift_tasks(
    session: AsyncSession,
    shift_tasks: list[ShiftTaskCreateSchema],
) -> list[ShiftTaskCreateSchema]:
    created_tasks = []
    for task_data in shift_tasks:
        task = ShiftTask(**task_data.dict())
        session.add(task)
        created_tasks.append(task_data)
    await session.commit()
    return created_tasks


async def update_shift_task(
    session: AsyncSession,
    task: ShiftTask,
    update_data: ShiftTaskUpdateSchema,
) -> ShiftTaskSchema:
    update_dict = update_data.dict(exclude_unset=True)

    if "is_closed" in update_dict:
        task.closed_at = datetime.now() if update_dict["is_closed"] else None

    for field, value in update_dict.items():
        setattr(task, field, value)

    await session.commit()
    await session.refresh(task)
    return ShiftTaskSchema.from_orm(task)
