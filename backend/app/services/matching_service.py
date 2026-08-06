class MatchingService:

    @staticmethod
    def calculate_score(candidate_skills, jd_skills):

        candidate = set(skill.lower() for skill in candidate_skills)
        required = set(skill.lower() for skill in jd_skills)

        matched = candidate.intersection(required)
        missing = required - candidate

        if len(required) == 0:
            score = 0
        else:
            score = round((len(matched) / len(required)) * 100, 2)

        return {
            "score": score,
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(missing))
        }