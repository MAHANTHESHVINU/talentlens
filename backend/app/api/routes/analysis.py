from fastapi import APIRouter

from app.services.resume_service import ResumeService
from app.services.extraction_service import ExtractionService
from app.services.jd_service import JDService
from app.services.matching_service import MatchingService
from app.services.recommendation_service import RecommendationService
from app.services.decision_service import DecisionService
from app.services.report_service import ReportService

router = APIRouter()

extractor = ExtractionService()


@router.get("/")
def analyze():

    # Load Job Description
    job_description = JDService.load_job_description()

    if not job_description:
        return {
            "success": False,
            "message": "No Job Description found in uploads/job_descriptions"
        }

    # Extract Job Description details
    jd_info = extractor.extract(job_description)

    # Load all resumes
    resumes = ResumeService.load_resumes()

    results = []

    for resume in resumes:

        # Extract resume information
        resume_info = extractor.extract(resume["text"])

        # Match with JD
        match = MatchingService.calculate_score(
            resume_info["skills"],
            jd_info["skills"]
        )

        # Recommendation
        recommendation = RecommendationService.get_recommendation(
            match["score"]
        )

        # AI Decision
        decision = DecisionService.generate({
            "score": match["score"],
            "matched_skills": match["matched_skills"],
            "missing_skills": match["missing_skills"]
        })

        candidate = {
            "filename": resume["filename"],
            "characters": resume["characters"],
            "email": resume_info["email"],
            "phone": resume_info["phone"],
            "skills": resume_info["skills"],
            "score": match["score"],
            "matched_skills": match["matched_skills"],
            "missing_skills": match["missing_skills"],
            "recommendation": recommendation,
            "ai_decision": decision
        }

        results.append(candidate)

    # Sort by highest score
    results.sort(
        key=lambda candidate: candidate["score"],
        reverse=True
    )

    # Top candidate
    top_candidate = results[0] if results else None

    response = {
        "success": True,
        "job_description": {
            "loaded": True,
            "characters": len(job_description),
            "skills": jd_info["skills"]
        },
        "top_candidate": top_candidate,
        "total_resumes": len(results),
        "resumes": results
    }

    # Generate reports automatically
    ReportService.generate(response)

    return response