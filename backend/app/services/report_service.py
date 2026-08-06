import json
from pathlib import Path

import pandas as pd


class ReportService:

    REPORT_DIR = Path("reports")

    @classmethod
    def generate(cls, response):

        cls.REPORT_DIR.mkdir(parents=True, exist_ok=True)

        json_file = cls.REPORT_DIR / "final_report.json"
        csv_file = cls.REPORT_DIR / "final_report.csv"

        # Save complete JSON report
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(response, f, indent=4)

        # Save candidate summary as CSV
        rows = []

        for candidate in response["resumes"]:
            rows.append({
                "Filename": candidate["filename"],
                "Score": candidate["score"],
                "Recommendation": candidate["recommendation"],
                "Email": candidate["email"],
                "Phone": candidate["phone"],
                "Matched Skills": ", ".join(candidate["matched_skills"]),
                "Missing Skills": ", ".join(candidate["missing_skills"]),
                "AI Decision": candidate["ai_decision"]
            })

        df = pd.DataFrame(rows)
        df.to_csv(csv_file, index=False)

        return {
            "json_report": str(json_file),
            "csv_report": str(csv_file)
        }