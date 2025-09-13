import json
import re
from .base import BaseAgent

class EvaluatorAgent(BaseAgent):
    def evaluate(self, question: str, answer: str):
        prompt = f"""
You are an expert Excel interviewer and evaluator.

Question: {question}
Candidate Answer: {answer}

Return a JSON object with these keys:
- score (1–5, numeric)
- justification (one-line reason for score)
- explanation (2–4 sentences explaining strengths and weaknesses of the answer)
- tip (one actionable improvement suggestion)
"""
        raw = self.ask_gemini(prompt)

        # --- CLEANUP STEP ---
        cleaned = re.sub(r"```json|```", "", raw).strip()

        try:
            obj = json.loads(cleaned)
            return {
                "score": str(obj.get("score", "N/A")),
                "justification": obj.get("justification", "").strip(),
                "explanation": obj.get("explanation", "").strip(),
                "tip": obj.get("tip", "").strip(),
            }
        except Exception:
            # Fallback if parsing fails
            return {
                "score": "3",
                "justification": "Could not parse structured evaluation.",
                "explanation": raw if raw else "No explanation provided.",
                "tip": "Provide concrete Excel examples next time.",
            }
