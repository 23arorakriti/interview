from .base import BaseAgent


class QuestionGeneratorAgent(BaseAgent):
    def generate(self, level="basic", n=3):
        prompt = f"Generate {n} {level} Excel interview questions as a numbered list."
        raw = self.ask_gemini(prompt)
        return [
            line.strip("1234567890. )") for line in raw.splitlines() if line.strip()
        ]
