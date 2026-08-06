from pathlib import Path
import re


class ExtractionService:

    def __init__(self):

        skills_path = Path("app/data/skills.txt")

        self.skills = [
            skill.strip().lower()
            for skill in skills_path.read_text(
                encoding="utf-8"
            ).splitlines()
            if skill.strip()
        ]

    def extract(self, text: str):

        lower = text.lower()

        found = []

        for skill in self.skills:

            # Normalize
            normalized_skill = (
                skill.replace(".", "")
                     .replace("-", " ")
                     .strip()
            )

            normalized_text = (
                lower.replace(".", "")
                     .replace("-", " ")
            )

            if normalized_skill in normalized_text:
                found.append(skill)

        email = self.extract_email(text)
        phone = self.extract_phone(text)

        return {
            "email": email,
            "phone": phone,
            "skills": sorted(list(set(found)))
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