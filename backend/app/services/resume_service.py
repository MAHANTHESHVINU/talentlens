from pathlib import Path

from app.parsers.resume_parser import ResumeParser


class ResumeService:

    RESUME_FOLDER = Path("uploads/resumes")

    @classmethod
    def load_resumes(cls):
        resumes = []

        for file in cls.RESUME_FOLDER.iterdir():

            if file.suffix.lower() not in [".pdf", ".docx", ".txt"]:
                continue

            text = ResumeParser.parse(str(file))

            resumes.append(
                {
                    "filename": file.name,
                    "text": text,
                    "characters": len(text),
                }
            )

        return resumes