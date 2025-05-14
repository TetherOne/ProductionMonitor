from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.production_monitor.api import router
from src.production_monitor.utils.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    """
    Закрываем соединение после завершения
    работы приложения
    """
    await db_helper.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
app.include_router(router)
