from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def analyze():
    return {
        "message": "Analysis endpoint working"
    }