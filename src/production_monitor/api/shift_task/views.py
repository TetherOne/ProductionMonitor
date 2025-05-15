from typing import Annotated

from fastapi import status, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.production_monitor.api.shift_task import crud
from src.production_monitor.api.shift_task.dependencies import shift_task_by_id
from src.production_monitor.api.shift_task.schemas import ShiftTaskSchema
from src.production_monitor.utils.db_helper import db_helper
from src.production_monitor.utils.filters import ShiftTaskFilterParams

router = APIRouter(tags=["Notes"])


@router.get(
    "/",
    response_model=list[ShiftTaskSchema],
    status_code=status.HTTP_200_OK,
)
async def get_shift_tasks(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    filters: Annotated[
        ShiftTaskFilterParams,
        Depends(),
    ],
):
    return await crud.get_shift_tasks(session=session, **filters.dict())


@router.get(
    "/{task_id}/",
    response_model=ShiftTaskSchema,
    status_code=status.HTTP_200_OK,
)
async def get_shift_task(
    shift_task: ShiftTaskSchema = Depends(shift_task_by_id),
):
    return shift_task
