import logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)
logging.getLogger("pdfplumber").setLevel(logging.ERROR)
from app.services.resume_service import ResumeService
from app.services.jd_service import JDService
from app.services.extraction_service import ExtractionService
from app.services.matching_service import MatchingService
from app.services.recommendation_service import RecommendationService
from app.services.decision_service import DecisionService
from app.services.report_service import ReportService

extractor = ExtractionService()


def main():

    print("=" * 70)
    print("          TalentLens AI Resume Screening Pipeline")
    print("=" * 70)

    print("\nLoading Job Description...")

    job_description = JDService.load_job_description()

    if not job_description:
        print("❌ No Job Description found.")
        return

    jd_info = extractor.extract(job_description)
    print("\nJD Skills Found:")
    print(jd_info["skills"])

    print("✅ Job Description Loaded")

    print("\nLoading Resumes...")

    resumes = ResumeService.load_resumes()
    for resume in resumes:
        print("\n" + "=" * 70)
        print(resume["filename"])
        print("=" * 70)
        print(resume["text"][:2000])

    print(f"✅ {len(resumes)} Resume(s) Loaded")

    results = []

    print("\nAnalyzing Candidates...\n")

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

        results.append({
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
        })

    results.sort(
        key=lambda candidate: candidate["score"],
        reverse=True
    )

    response = {
        "success": True,
        "job_description": {
            "loaded": True,
            "characters": len(job_description),
            "skills": jd_info["skills"]
        },
        "top_candidate": results[0] if results else None,
        "total_resumes": len(results),
        "resumes": results
    }

    reports = ReportService.generate(response)

    print("=" * 70)
    print("Candidate Rankings")
    print("=" * 70)

    for index, candidate in enumerate(results, start=1):

        print(f"\nRank #{index}")
        print(f"Resume         : {candidate['filename']}")
        print(f"Score          : {candidate['score']}%")
        print(f"Recommendation : {candidate['recommendation']}")
        print(f"Matched Skills : {', '.join(candidate['matched_skills'])}")
        print(f"Missing Skills : {', '.join(candidate['missing_skills'])}")
        print(f"AI Decision    : {candidate['ai_decision']}")

    print("\n" + "=" * 70)
    print("Pipeline Completed Successfully")
    print("=" * 70)

    print(f"\nTop Candidate : {response['top_candidate']['filename']}")
    print(f"Top Score     : {response['top_candidate']['score']}%")

    print("\nReports Generated")

    print(f"JSON : {reports['json_report']}")
    print(f"CSV  : {reports['csv_report']}")

    print("\nThank you for using TalentLens AI.")


if __name__ == "__main__":
    main()