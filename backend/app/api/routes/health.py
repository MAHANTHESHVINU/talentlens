from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health():
    return {
        "status": "healthy",
        "service": "TalentLens AI",
        "version": "1.0.0"
    }