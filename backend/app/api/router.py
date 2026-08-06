from fastapi import APIRouter

from app.api.routes import (
    health,
    upload,
    analysis,
    results,
)

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(upload.router, prefix="/upload", tags=["Upload"])
router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
router.include_router(results.router, prefix="/results", tags=["Results"])