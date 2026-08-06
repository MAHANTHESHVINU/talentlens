from pathlib import Path


class JDParser:

    @staticmethod
    def parse(file_path: str) -> str:
        path = Path(file_path)

        if path.suffix.lower() == ".txt":
            return path.read_text(encoding="utf-8")

        raise ValueError("Unsupported JD format")