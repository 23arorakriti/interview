from .base import BaseAgent


class FeedbackAgent(BaseAgent):
    def summarize(self, evaluations):
        eval_text = "\n".join(
            [
                f"Q{i+1}: {ev['justification']} (Score {ev['score']})"
                for i, ev in enumerate(evaluations)
            ]
        )
        prompt = f"""
Given these evaluations:

{eval_text}

Write a 120-word summary of strengths, weaknesses, and a hire/not-hire recommendation.
"""
        return self.ask_gemini(prompt)
