from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.routes.auth import AUTH_REQUIRED, require_authenticated_user
from app.parsers.resume_parser import ResumeParser
from app.services.upload_service import parse_uploaded_file

router = APIRouter()

UPLOAD_DIR = Path("uploads/resumes")
MAX_RESUME_FILES = 25


@router.post("/resumes")
async def upload_resumes(
    files: Annotated[list[UploadFile], File()],
    user: dict = Depends(require_authenticated_user),
):
    if len(files) > MAX_RESUME_FILES:
        raise HTTPException(
            status_code=413,
            detail=f"A request can contain at most {MAX_RESUME_FILES} resumes.",
        )

    results = []

    for file in files:
        filename, content, text = await parse_uploaded_file(
            file,
            ResumeParser.parse,
            {".pdf", ".docx", ".txt"},
        )
        if not AUTH_REQUIRED:
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            (UPLOAD_DIR / filename).write_bytes(content)

        results.append(
            {
                "filename": filename,
                "characters": len(text),
                "preview": text[:200],
            }
        )

    return {
        "uploaded": len(results),
        "results": results,
    }