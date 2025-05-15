from fastapi import APIRouter

from src.production_monitor.api.product_code.views import router as product_code_router
from src.production_monitor.settings.config import settings

router = APIRouter()

router.include_router(
    product_code_router,
    prefix=settings.api.product_codes,
)
