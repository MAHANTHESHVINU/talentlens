from fastapi import APIRouter

from app.services.resume_service import ResumeService
from app.services.extraction_service import ExtractionService
from app.services.jd_service import JDService
from app.services.matching_service import MatchingService

router = APIRouter()

extractor = ExtractionService()


@router.get("/")
def analyze():

    # Load Job Description
    job_description = JDService.load_job_description()

    if not job_description:
        return {
            "message": "No Job Description found in uploads/job_descriptions"
        }

    # Extract JD information
    jd_info = extractor.extract(job_description)

    # Load resumes
    resumes = ResumeService.load_resumes()

    results = []

    for resume in resumes:

        # Extract resume information
        resume_info = extractor.extract(resume["text"])

        # Calculate match score
        match = MatchingService.calculate_score(
            resume_info["skills"],
            jd_info["skills"]
        )

        results.append({
            "filename": resume["filename"],
            "characters": resume["characters"],
            "email": resume_info["email"],
            "phone": resume_info["phone"],
            "skills": resume_info["skills"],
            "score": match["score"],
            "matched_skills": match["matched_skills"],
            "missing_skills": match["missing_skills"]
        })

    # Rank candidates by score
    results.sort(
        key=lambda candidate: candidate["score"],
        reverse=True
    )

    return {
        "job_description": {
            "loaded": True,
            "characters": len(job_description),
            "skills": jd_info["skills"]
        },
        "total_resumes": len(results),
        "resumes": results
    }