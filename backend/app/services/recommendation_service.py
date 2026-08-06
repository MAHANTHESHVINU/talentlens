class RecommendationService:

    @staticmethod
    def get_recommendation(score: float):

        if score >= 90:
            return "Excellent Match"

        if score >= 75:
            return "Strong Match"

        if score >= 60:
            return "Good Match"

        if score >= 40:
            return "Average Match"

        return "Poor Match"