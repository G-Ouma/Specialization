import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Locate the shared .env file at the Specialization root
ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(ENV_PATH)

# Load Gemini configuration
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY was not found in the root .env file.")

if not MODEL:
    raise ValueError("GEMINI_MODEL was not found in the root .env file.")

# Initialise Gemini client
client = genai.Client(api_key=API_KEY)


def answer_question(question, retrieved_chunks):
    """
    Generate an answer using only the retrieved PDF passages.
    Include page references in the answer.
    """

    if not retrieved_chunks:
        return "I couldn't find relevant information in the document to answer that question."

    # Prepare the complete retrieved passages
    context = ""

    for index, chunk in enumerate(retrieved_chunks, start=1):
        context += (
            f"\nPassage {index} (PDF page {chunk['page']}):\n"
            f"{chunk['text']}\n"
        )

    prompt = f"""
        You are a PDF question-answering assistant.

        Answer the user's question using only the information in the
        provided PDF passages.

        Instructions:
        1. Use only the information in the provided PDF passages.
        2. Give a clear, direct and informative answer.
        3. Explain relevant ideas rather than simply copying passages.
        4. Cite sources using PDF page numbers only, e.g. (PDF page 70).
        5. Never refer to passages by their internal numbers.
        6. If the passages do not contain enough information, say so.
        7. Distinguish between the author's explicit statements and
        reasonable conclusions drawn from the text.
        8. Do not invent quotations, page references or details.

        PDF PASSAGES: {context}

        USER QUESTION: {question}

        ANSWER:
        """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    if not response.text:
        return "Gemini did not generate an answer. Please try again."

    return response.text.strip()