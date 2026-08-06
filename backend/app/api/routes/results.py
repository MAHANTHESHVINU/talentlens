from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def results():
    return {
        "message": "Results endpoint working"
    }