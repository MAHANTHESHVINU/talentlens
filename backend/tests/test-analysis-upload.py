from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analysis_accepts_uploaded_jd_and_resume_files():
    jd_path = Path("uploads/job_descriptions/software_engineer.txt")
    resume_path = Path("uploads/resumes/Software Engineer Resume.pdf")

    with jd_path.open("rb") as jd_file, resume_path.open("rb") as resume_file:
        response = client.post(
            "/analysis/",
            files={
                "job_description": ("software_engineer.txt", jd_file, "text/plain"),
                "resumes": (
                    "Software Engineer Resume.pdf",
                    resume_file,
                    "application/pdf",
                ),
            },
        )

    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["success"] is True
    assert payload["job_description"]["loaded"] is True
    assert payload["total_resumes"] == 1
    assert payload["resumes"][0]["filename"] == "Software Engineer Resume.pdf"
