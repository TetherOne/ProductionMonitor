from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.production_monitor.api.shift_task.schemas import ShiftTaskSchema
from src.production_monitor.models import ShiftTask


async def get_shift_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> ShiftTaskSchema | None:
    stmt = select(ShiftTask).where(ShiftTask.id == task_id)
    result = await session.scalar(stmt)
    return result
