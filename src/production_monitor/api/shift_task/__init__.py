from fastapi import APIRouter

from src.production_monitor.api.shift_task.views import router as shift_task_router
from src.production_monitor.settings.config import settings

router = APIRouter()

router.include_router(
    shift_task_router,
    prefix=settings.api.shift_tasks,
)
