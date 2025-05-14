from fastapi import status, APIRouter, Depends

from src.production_monitor.api.shift_task.dependencies import shift_task_by_id
from src.production_monitor.api.shift_task.schemas import ShiftTaskSchema

router = APIRouter(tags=["Notes"])


@router.get(
    "/{task_id}/",
    response_model=ShiftTaskSchema,
    status_code=status.HTTP_200_OK,
)
async def get_shift_task(
    shift_task: ShiftTaskSchema = Depends(shift_task_by_id),
):
    return shift_task
