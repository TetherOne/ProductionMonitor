from typing import Annotated

from fastapi import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.production_monitor.api.shift_task import crud
from src.production_monitor.api.shift_task.schemas import ShiftTaskSchema
from src.production_monitor.utils.db_helper import db_helper
from src.production_monitor.utils.errors import NotFound


async def shift_task_by_id(
    task_id: Annotated[int, Path],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> ShiftTaskSchema:
    shift_task = await crud.get_shift_task_by_id(
        session=session,
        task_id=task_id,
    )
    if shift_task is not None:
        return shift_task
    raise NotFound()
