from pathlib import Path
import re


class ExtractionService:

    def __init__(self):

        skills_path = Path("app/data/skills.txt")

        self.skills = {
            skill.strip().lower()
            for skill in skills_path.read_text().splitlines()
            if skill.strip()
        }

    def extract(self, text: str):

        lower = text.lower()

        found = sorted([
            skill
            for skill in self.skills
            if skill in lower
        ])

        email = self.extract_email(text)
        phone = self.extract_phone(text)

        return {
            "email": email,
            "phone": phone,
            "skills": found
        }

    @staticmethod
    def extract_email(text):

        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        return match.group() if match else None

    @staticmethod
    def extract_phone(text):

        match = re.search(
            r"(?:\+91[- ]?)?[6-9]\d{9}",
            text
        )

        return match.group() if match else None