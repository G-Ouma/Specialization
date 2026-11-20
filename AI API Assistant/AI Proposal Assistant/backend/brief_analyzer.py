import os
import json

from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

from backend.prompts import BRIEF_ANALYSIS_PROMPT


# Load environment variables from project root
SPECIALIZATION_ROOT = Path(__file__).resolve().parents[3]

ENV_FILE = SPECIALIZATION_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)


def analyze_brief(brief: str):

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing.")

    if not model:
        raise ValueError("GEMINI_MODEL is missing.")

    try:
        with genai.Client(api_key=api_key) as client:

            response = client.models.generate_content(
                model=model,
                contents=brief,
                config=types.GenerateContentConfig(
                    system_instruction=BRIEF_ANALYSIS_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.2,
                    max_output_tokens=1500
                )
            )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        analysis = json.loads(response.text)

        return analysis

    except json.JSONDecodeError as error:
        raise ValueError(
            "Gemini returned an invalid JSON response."
        ) from error