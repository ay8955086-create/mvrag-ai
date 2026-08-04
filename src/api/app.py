"""
FastAPI application for MVRAG AI.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

import src.models

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.upload import router as upload_router
from src.api.routers.query import router as query_router
from src.api.routers.health import router as health_router

from src.config.settings import settings
from src.core.logger import get_logger
from src.database.init_db import (
    check_database_connection,
    initialize_database,
)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown.
    """

    logger.info("=" * 60)
    logger.info("Starting %s", settings.APP_NAME)

    try:
        check_database_connection()
        initialize_database()

        logger.info("Database initialized successfully.")
        logger.info("Application startup completed.")

    except Exception:
        logger.exception("Application startup failed.")
        raise

    yield

    logger.info("Application shutdown completed.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multimodal Video Retrieval-Augmented Generation",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# ------------------------------------------------------------
# Routers
# ------------------------------------------------------------

app.include_router(upload_router)
app.include_router(query_router)
app.include_router(health_router)

# ------------------------------------------------------------
# CORS
# ------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Root
# ------------------------------------------------------------

@app.get("/", tags=["Root"])
async def root():

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }