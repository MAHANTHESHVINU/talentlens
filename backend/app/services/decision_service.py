class DecisionService:

    @staticmethod
    def generate(candidate):

        score = candidate["score"]
        missing = candidate["missing_skills"]
        matched = candidate["matched_skills"]

        if score >= 90:
            return (
                f"Excellent candidate. Matched {len(matched)} required skills. "
                "Recommended for immediate interview."
            )

        if score >= 75:
            return (
                f"Strong candidate with {len(matched)} matching skills. "
                f"Consider improving: {', '.join(missing) if missing else 'None'}."
            )

        if score >= 60:
            return (
                f"Good candidate but missing important skills: "
                f"{', '.join(missing)}."
            )

        if score >= 40:
            return (
                f"Average fit. Candidate lacks several required skills: "
                f"{', '.join(missing)}."
            )

        return (
            f"Poor match. Missing most required skills: "
            f"{', '.join(missing)}."
        )