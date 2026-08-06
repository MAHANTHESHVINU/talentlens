from fastapi import APIRouter

from app.services.resume_service import ResumeService

router = APIRouter()


@router.get("/")
def analyze():

    resumes = ResumeService.load_resumes()

    return {
        "total_resumes": len(resumes),
        "resumes": resumes,
    }