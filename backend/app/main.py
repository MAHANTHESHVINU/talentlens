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
        "status": "success",
        "message": f"{settings.APP_NAME} API is running 🚀",
    }