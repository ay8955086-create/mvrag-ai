"""
FastAPI application for MVRAG AI.
"""

from __future__ import annotations

import src.models

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.video import router as video_router
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
app.include_router(video_router)

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
# Root Endpoint
# ------------------------------------------------------------

@app.get("/", tags=["Root"])
async def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


# ------------------------------------------------------------
# Health Endpoint
# ------------------------------------------------------------

@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "database": "connected",
    }