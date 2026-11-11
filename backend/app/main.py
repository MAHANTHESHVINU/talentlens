import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.api.router import router
from app.api.routes.auth import (
    SESSION_COOKIE_SECURE,
    SESSION_SECRET,
    validate_auth_configuration,
)
from app.core.config import settings
from app.core.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Resume Screening Agent",
)

frontend_origins = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:8001,http://127.0.0.1:8001,"
    "http://localhost:3000,http://127.0.0.1:3000,"
    "http://localhost:5173,http://127.0.0.1:5173",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in frontend_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET or "local-development-only-session-secret",
    same_site="lax",
    https_only=SESSION_COOKIE_SECURE,
    max_age=8 * 60 * 60,
)

app.include_router(router)


@app.get("/api")
def root():
    return {
        "project": "TalentLens AI",
        "version": "1.0.0",
        "status": "Running",
        "api_docs": "/docs",
        "analysis_endpoint": "/analysis/"
    }


frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount(
    "/",
    StaticFiles(directory=str(frontend_dir), html=True),
    name="dashboard",
)


@app.on_event("startup")
def startup():
    validate_auth_configuration()
    logger.info("TalentLens AI started successfully.")