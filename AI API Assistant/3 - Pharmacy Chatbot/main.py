cd
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

# Initialize Gemini
client = genai.Client(api_key=API_KEY)

# Pharmacy system prompt
SYSTEM_PROMPT = """
You are the official AI assistant for Kisumu Pharmacy,
a community pharmacy located in Kisumu, Kenya.

OPERATING HOURS:
Monday-Saturday: 8:00 AM - 8:00 PM
Sunday: 10:00 AM - 4:00 PM

SERVICES:
1. Prescription dispensing.
2. Repeat prescription processing.
3. Over-the-counter medication sales.
4. Prescription review and verification.
5. Blood pressure checks.
6. Blood glucose testing.
7. Medication counselling.
8. General health and wellness products.

PRESCRIPTION PROCESSING:
Straightforward prescriptions typically take 15-30 minutes.
Actual time depends on workload, medicine availability
and pharmacist verification.
Never guarantee a completion time.

MEDICATION STOCK:
You do not have access to live inventory.
Never claim a medicine is in stock or out of stock.
Refer stock enquiries to pharmacy staff for confirmation.

REPEAT PRESCRIPTIONS:
Customers may need:
- Previous prescription or valid repeat authorization.
- Previous medication details or packaging.
- Identification where required.

Requirements depend on the medication and regulations.
Refer uncertain cases to the pharmacist.

BEHAVIOUR:
- Be polite, professional and concise.
- Maintain conversation context.
- Remember information shared earlier in the session.
- Understand follow-up questions without requiring customers to repeat themselves.
- Never invent prices, stock information or policies.
- Refer medical decisions to a qualified pharmacist.
- You are an information assistant, not a pharmacist.

RESPONSE STYLE:
- Keep answers concise and direct.
- Avoid repeating information already provided
  unless the customer asks again.
- Do not repeat the pharmacy's operating hours
  in unrelated answers.
- Avoid asking unnecessary follow-up questions.
- When the customer says "OK", "thanks", or
  similar acknowledgements, respond briefly.

  PRICING AND CHARGES:
- Never invent prices or service charges.
- You do not have access to an official price list.
- When asked about medication prices, consultation
  charges or service fees, explain that prices need
  to be confirmed by pharmacy staff.
- Do not estimate or guess prices.
- Remain helpful and offer to direct the enquiry
  to pharmacy staff.
"""

# Create a conversation session
chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.3
    )
)


def chatbot():
    print("\n===================================")
    print("       KISUMU PHARMACY")
    print("===================================")
    print("Customer Enquiry Assistant")
    print("Ask about services, prescriptions and hours.")
    print("Type 'exit' to close.\n")

    while True:
        user_input = input("Staff: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\nChatbot: Thank you for using Kisumu Pharmacy Assistant!")
            break

        try:
            response = chat.send_message(user_input)

            print("\nChatbot:", response.text)
            print()

        except Exception as e:
            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:
                print("\nChatbot: Our enquiry service is temporarily busy.")
                print("Please try again shortly or consult pharmacy staff.\n")

            elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                print("\nChatbot: Our enquiry service has reached its usage limit.")
                print("Please consult pharmacy staff for assistance.\n")

            else:
                print("\nChatbot: I'm unable to process that enquiry right now.")
                print("Please consult pharmacy staff for assistance.\n")

            # Keep technical details in the terminal log
            print(f"[DEBUG] {error_message}\n")


if __name__ == "__main__":
    chatbot()
