from typing import Annotated

from fastapi import status, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.production_monitor.api.shift_task import crud
from src.production_monitor.api.shift_task.dependencies import shift_task_by_id
from src.production_monitor.api.shift_task.schemas import (
    ShiftTaskSchema,
    ShiftTaskCreateSchema,
    ShiftTaskUpdateSchema,
)
from src.production_monitor.models import ShiftTask
from src.production_monitor.utils.db_helper import db_helper
from src.production_monitor.utils.filters import ShiftTaskFilterParams

router = APIRouter(tags=["Shift Tasks"])


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
    return await crud.get_shift_tasks(
        session=session,
        **filters.model_dump(),
    )


@router.get(
    "/{task_id}/",
    response_model=ShiftTaskSchema,
    status_code=status.HTTP_200_OK,
)
async def get_shift_task(
    shift_task: Annotated[
        ShiftTaskSchema,
        Depends(shift_task_by_id),
    ],
):
    return shift_task


@router.post(
    "/create/",
    response_model=list[ShiftTaskCreateSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_shift_tasks(
    shift_tasks: list[ShiftTaskCreateSchema],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.create_shift_tasks(
        session=session,
        shift_tasks=shift_tasks,
    )


@router.patch(
    "/{task_id}/update/",
    response_model=ShiftTaskSchema,
    status_code=status.HTTP_200_OK,
)
async def update_shift_task(
    update_data: ShiftTaskUpdateSchema,
    task: Annotated[
        ShiftTask,
        Depends(shift_task_by_id),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.update_shift_task(
        session=session,
        task=task,
        update_data=update_data,
    )
