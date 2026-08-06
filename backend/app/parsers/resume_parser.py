from pathlib import Path
import pdfplumber
from docx import Document


class ResumeParser:

    @staticmethod
    def parse(file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return ResumeParser._parse_pdf(file_path)

        if extension == ".docx":
            return ResumeParser._parse_docx(file_path)

        if extension == ".txt":
            return ResumeParser._parse_txt(file_path)

        return ""

    @staticmethod
    def _parse_pdf(file_path):
        text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text

    @staticmethod
    def _parse_docx(file_path):
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    @staticmethod
    def _parse_txt(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()