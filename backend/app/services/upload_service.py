import tempfile
from pathlib import Path
from typing import Callable

from fastapi import HTTPException, UploadFile

MAX_UPLOAD_SIZE = 10 * 1024 * 1024


async def parse_uploaded_file(
    upload: UploadFile,
    parser: Callable[[str], str],
    allowed_extensions: set[str],
) -> tuple[str, bytes, str]:
    original_name = (upload.filename or "").replace("\\", "/").rsplit("/", 1)[-1]
    extension = Path(original_name).suffix.lower()
    if not original_name or extension not in allowed_extensions:
        supported = ", ".join(sorted(allowed_extensions))
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type. Supported extensions: {supported}.",
        )

    content = await upload.read(MAX_UPLOAD_SIZE + 1)
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"{original_name} exceeds the 10 MB per-file limit.",
        )
    if not content:
        raise HTTPException(status_code=400, detail=f"{original_name} is empty.")

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as temporary:
            temporary.write(content)
            temporary_path = temporary.name
        text = parser(temporary_path)
    finally:
        if temporary_path:
            Path(temporary_path).unlink(missing_ok=True)

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail=f"No readable text was found in {original_name}.",
        )

    return original_name, content, text
