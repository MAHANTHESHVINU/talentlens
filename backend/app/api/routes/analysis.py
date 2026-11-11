from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.routes.auth import AUTH_REQUIRED, require_authenticated_user
from app.parsers.jd_parser import JDParser
from app.parsers.resume_parser import ResumeParser
from app.services.resume_service import ResumeService
from app.services.extraction_service import ExtractionService
from app.services.jd_service import JDService
from app.services.matching_service import MatchingService
from app.services.recommendation_service import RecommendationService
from app.services.decision_service import DecisionService
from app.services.report_service import ReportService
from app.services.upload_service import parse_uploaded_file

router = APIRouter()

extractor = ExtractionService()
MAX_RESUME_FILES = 25


def _build_analysis_response(
    job_description: str,
    resumes: list[dict],
    persist_reports: bool = True,
):
    jd_info = extractor.extract(job_description)

    results = []

    for resume in resumes:
        resume_info = extractor.extract(resume["text"])

        match = MatchingService.calculate_score(
            resume_info["skills"],
            jd_info["skills"]
        )

        recommendation = RecommendationService.get_recommendation(
            match["score"]
        )

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

    results.sort(
        key=lambda candidate: candidate["score"],
        reverse=True
    )

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

    if persist_reports:
        ReportService.generate(response)
    return response


@router.get("/")
def analyze(user: dict = Depends(require_authenticated_user)):
    if AUTH_REQUIRED:
        raise HTTPException(
            status_code=403,
            detail="Folder-based analysis is disabled. Upload files for each screening.",
        )

    job_description = JDService.load_job_description()

    if not job_description:
        return {
            "success": False,
            "message": "No Job Description found in uploads/job_descriptions"
        }

    resumes = ResumeService.load_resumes()
    return _build_analysis_response(job_description, resumes)


@router.post("/")
async def analyze_uploaded_files(
    job_description: UploadFile = File(default=None),
    resumes: list[UploadFile] = File(default_factory=list),
    user: dict = Depends(require_authenticated_user),
):
    if job_description is not None:
        filename, content, job_text = await parse_uploaded_file(
            job_description,
            JDParser.parse,
            JDService.SUPPORTED_EXTENSIONS,
        )
        if not AUTH_REQUIRED:
            jd_dir = JDService.JD_FOLDER
            jd_dir.mkdir(parents=True, exist_ok=True)
            (jd_dir / filename).write_bytes(content)
    else:
        if AUTH_REQUIRED:
            raise HTTPException(
                status_code=400,
                detail="Upload a job description for this screening.",
            )
        job_text = JDService.load_job_description()

    if not job_text:
        raise HTTPException(
            status_code=400,
            detail="No job description uploaded or found in uploads/job_descriptions.",
        )

    uploaded_resumes = []

    if resumes:
        if len(resumes) > MAX_RESUME_FILES:
            raise HTTPException(
                status_code=413,
                detail=f"A screening can contain at most {MAX_RESUME_FILES} resumes.",
            )

        resume_dir = ResumeService.RESUME_FOLDER
        if not AUTH_REQUIRED:
            resume_dir.mkdir(parents=True, exist_ok=True)

        for resume_file in resumes:
            filename, content, resume_text = await parse_uploaded_file(
                resume_file,
                ResumeParser.parse,
                {".pdf", ".docx", ".txt"},
            )
            if not AUTH_REQUIRED:
                (resume_dir / filename).write_bytes(content)

            uploaded_resumes.append({
                "filename": filename,
                "text": resume_text,
                "characters": len(resume_text),
            })
    else:
        if AUTH_REQUIRED:
            raise HTTPException(
                status_code=400,
                detail="Upload at least one resume for this screening.",
            )
        uploaded_resumes = ResumeService.load_resumes()

    if not uploaded_resumes:
        raise HTTPException(
            status_code=400,
            detail="No resume files uploaded or found in uploads/resumes.",
        )

    return _build_analysis_response(
        job_text,
        uploaded_resumes,
        persist_reports=not AUTH_REQUIRED,
    )