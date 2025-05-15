from fastapi import APIRouter

from src.production_monitor.api.shift_task import router as shift_task_router
from src.production_monitor.api.product_code import router as product_code_router


from src.production_monitor.settings.config import settings

router = APIRouter(
    prefix=settings.api.full_prefix,
)

router.include_router(shift_task_router)
router.include_router(product_code_router)
