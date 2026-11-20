
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from backend.prompts import PROPOSAL_GENERATION_PROMPT
from backend.pricing import calculate_project_price


# Load the shared environment file
SPECIALIZATION_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = SPECIALIZATION_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)


def generate_proposal(brief: str, analysis: dict) -> str:
    """
    Generate a tailored freelance proposal using the
    original client brief and its structured analysis.
    """

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing.")

    if not model:
        raise ValueError("GEMINI_MODEL is missing.")

    # Calculate pricing and delivery only when effort is reliable.
    effort = analysis.get("effort_estimate", {})

    pricing = None

    if (
        effort.get("working_days") is not None
        and not effort.get("needs_scoping", True)
    ):
        pricing = calculate_project_price(
            estimated_days=effort["working_days"]
        )

    if pricing:
        pricing_information = f"""
        CALCULATED PROJECT COMMERCIAL TERMS:

        Currency: {pricing['currency']}
        Estimated working effort: {pricing['estimated_days']} working days
        Proposed delivery duration: {pricing['delivery_days']} working days
        Daily rate: {pricing['daily_rate']}
        Minimum project fee: {pricing['minimum_project_fee']}
        Final quotation: {pricing['currency']} {pricing['final_price']}
        Payment terms: {pricing['payment_terms']}

        STRICT INSTRUCTIONS:
        - Use the exact calculated project fee.
        - State the proposed delivery duration as exactly
          {pricing['delivery_days']} working days.
        - Do not calculate, modify, shorten, or extend these figures.
        - Do not confuse estimated effort with delivery duration.
        - The client's requested deadline is not the delivery duration.
        - Do not invent additional commercial terms.
        """
    else:
        pricing_information = """
        PRICING STATUS: NOT YET AVAILABLE.

        The project effort cannot currently be estimated reliably.
        Do not invent a price or delivery timeline.
        Explain briefly that scoping is required before a firm quotation
        and delivery duration can be provided.
        """

    prompt = f"""
    ORIGINAL CLIENT BRIEF:
    {brief}

    STRUCTURED BRIEF ANALYSIS:
    {analysis}

    PRICING INFORMATION:
    {pricing_information}

    Write a complete freelance proposal using the instructions
    provided. The proposal must not exceed 200 words.
    """

    try:
        with genai.Client(api_key=api_key) as client:

            for attempt in range(2):

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=PROPOSAL_GENERATION_PROMPT,
                        temperature=0.4,
                        max_output_tokens=1200
                    )
                )

                if not response.text:
                    raise ValueError("Gemini returned an empty proposal.")

                proposal = response.text.strip()
                word_count = len(proposal.split())

                if word_count <= 200:
                    return proposal

                if attempt == 0:
                    print(
                        f"Proposal contains {word_count} words. "
                        "Retrying with a stricter word limit..."
                    )

                    prompt += f"""

                    REVISION REQUIRED:

                    Your previous proposal contained {word_count} words.
                    Rewrite it to contain no more than 200 words,
                    including all six section headings.

                    Preserve the original brief, exact calculated price,
                    exact proposed delivery duration, assumptions and payment terms.
                    Do not invent or modify commercial figures.
                    """

            raise ValueError(
                "Gemini could not generate a proposal within 200 words "
                "after two attempts."
            )

        return proposal

    except Exception as error:
        raise RuntimeError(
            f"Proposal generation failed: {error}"
        ) from error