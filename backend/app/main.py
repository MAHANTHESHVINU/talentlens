from fastapi import FastAPI

from app.api.router import router
from app.core.config import settings
from app.core.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Resume Screening Agent",
)

app.include_router(router)


@app.on_event("startup")
def startup():
    logger.info("TalentLens AI started successfully.")


@app.get("/")
def root():
    return {
        "project": "TalentLens AI",
        "version": "1.0.0",
        "status": "Running",
        "api_docs": "/docs",
        "analysis_endpoint": "/analysis/"
    }