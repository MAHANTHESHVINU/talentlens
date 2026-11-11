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


def test_analysis_can_disable_shared_upload_and_report_persistence(tmp_path, monkeypatch):
    from app.api.routes import analysis

    monkeypatch.setattr(analysis, "PERSIST_SCREENING_DATA", False)
    monkeypatch.setattr(analysis.JDService, "JD_FOLDER", tmp_path / "job_descriptions")
    monkeypatch.setattr(analysis.ResumeService, "RESUME_FOLDER", tmp_path / "resumes")

    response = client.post(
        "/analysis/",
        files={
            "job_description": (
                "role.txt",
                b"Looking for Python and SQL experience.",
                "text/plain",
            ),
            "resumes": (
                "candidate.txt",
                b"Candidate with Python and SQL experience.",
                "text/plain",
            ),
        },
    )

    assert response.status_code == 200, response.text
    assert response.json()["total_resumes"] == 1
    assert not (tmp_path / "job_descriptions").exists()
    assert not (tmp_path / "resumes").exists()
    assert client.get("/analysis/").status_code == 403
