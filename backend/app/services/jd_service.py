from pathlib import Path

from app.parsers.jd_parser import JDParser


class JDService:

    JD_FOLDER = Path("uploads/job_descriptions")

    SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}

    @classmethod
    def load_job_description(cls):

        if not cls.JD_FOLDER.exists():
            return None

        for file in cls.JD_FOLDER.iterdir():

            if (
                file.is_file()
                and file.suffix.lower() in cls.SUPPORTED_EXTENSIONS
            ):
                return JDParser.parse(str(file))

        return None