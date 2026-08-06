from pathlib import Path

from app.parsers.jd_parser import JDParser


class JDService:

    JD_FOLDER = Path("uploads/job_descriptions")

    @classmethod
    def load_job_description(cls):

        files = list(cls.JD_FOLDER.glob("*"))

        if not files:
            return None

        return JDParser.parse(str(files[0]))