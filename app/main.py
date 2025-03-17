from contextlib import asynccontextmanager

from api.api import router as api_router
from core.config import settings
from fastapi import FastAPI
from loguru import logger
from services.common import close_connections, initialize_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Application startup with {settings.APP_MODE}.")
    await initialize_services()
    yield
    await close_connections()
    logger.info("Application is shutting down. Resources have been cleaned up.")

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
