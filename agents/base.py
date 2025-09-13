import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ensure .env is loaded
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Put it in your .env file.")

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-1.5-flash"


class BaseAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    def ask_gemini(self, prompt: str) -> str:
        try:
            resp = self.model.generate_content(prompt)
            return resp.text.strip()
        except Exception as e:
            return f"[Gemini error: {e}]"
