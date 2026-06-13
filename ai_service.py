from dotenv import load_dotenv
from google import genai

import os


# =====================================
# Configuration
# =====================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =====================================
# Gemini Service
# =====================================

def ask_gemini(prompt: str) -> str:

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text