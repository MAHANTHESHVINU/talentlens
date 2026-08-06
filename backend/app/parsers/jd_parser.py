from pathlib import Path

import pdfplumber
from docx import Document


class JDParser:

    @staticmethod
    def parse(file_path: str) -> str:

        path = Path(file_path)

        extension = path.suffix.lower()

        if extension == ".txt":
            return path.read_text(encoding="utf-8")

        elif extension == ".pdf":

            text = ""

            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            return text

        elif extension == ".docx":

            doc = Document(path)

            return "\n".join(
                paragraph.text
                for paragraph in doc.paragraphs
            )

        raise ValueError(f"Unsupported JD format: {extension}")