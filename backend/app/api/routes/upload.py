from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def upload():
    return {
        "message": "Upload endpoint working"
    }