from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from app.parsers.resume_parser import ResumeParser

router = APIRouter()

UPLOAD_DIR = Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/resumes")
async def upload_resumes(
    files: Annotated[list[UploadFile], File()]
):
    results = []

    for file in files:
        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = ResumeParser.parse(str(file_path))

        results.append(
            {
                "filename": file.filename,
                "characters": len(text),
                "preview": text[:200],
            }
        )

    return {
        "uploaded": len(results),
        "results": results,
    }