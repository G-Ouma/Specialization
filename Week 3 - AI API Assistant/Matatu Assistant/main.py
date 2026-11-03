"""Command-line AI assistant for a sample Thika Matatu SACCO."""
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-2.5-flash"

# DEMO DATA ONLY. Replace these values with approved SACCO records before use.
SYSTEM_PROMPT = """
You are a helpful, polite secretary assistant for a matatu SACCO based in Thika, Kenya.
Answer member questions clearly and briefly. Use Kenyan shillings (KSh).
The following are the SACCO's current SAMPLE information. Treat them as the source of truth:

1. MEMBER BALANCE:
   The demo member account is THK-014. Its sample outstanding balance is KSh 3,500
   as at 3 November 2026. This is demonstration data, not a live account lookup.
   If a person asks for their own balance but has not identified themselves, explain
   that this demo can only show the sample THK-014 balance and that the secretary
   must verify a real member's account before sharing personal financial information.

2. NEXT MEETING:
   The next general members' meeting is Friday, 13 November 2026, at 10:00 a.m.
   Venue: the SACCO office in Thika. Members should arrive 15 minutes early.

3. MEMBERSHIP FEES:
   One-time registration fee: KSh 500.
   One-time joining fee: KSh 2,000.
   Monthly membership contribution: KSh 1,000.

Rules:
- Answer only from the information above.
- Do not invent member balances, dates, venues, charges, or policies.
- If a question is unrelated or the answer is not listed, say the secretary should confirm it.
- Never claim to have checked a live account or SACCO database.
- Be friendly, professional, and easy to understand.
"""

def answer_question(question: str) -> str:
    """Send one member question to Gemini and return the assistant's answer."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to a .env file; see .env.example."
        )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
        ),
    )

    answer = response.text
    if not answer:
        return "Sorry, I couldn't generate an answer. Please ask the secretary."
    return answer.strip()


def main() -> None:
    print("\nTHIKA MATATU SACCO — MEMBER ASSISTANT")
    print("Ask about your balance, the next meeting, or membership fees.")
    print("Type 'exit' to close.\n")

    while True:
        try:
            question = input("Member: ").strip()
            if question.lower() in {"exit", "quit"}:
                print("Assistant: Goodbye!")
                break
            if not question:
                print("Assistant: Please type a question.\n")
                continue

            print("\nAssistant:", answer_question(question), "\n")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as error:
            print(f"\nAssistant: Sorry, something went wrong: {error}\n")


if __name__ == "__main__":
    main()
