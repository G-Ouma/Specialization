
import os
import json
import gspread
import traceback

from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)


# 1. Structured system prompt
SYSTEM_PROMPT = """
You are a property inquiry extraction assistant
working for a real estate agent in Nairobi, Kenya.

Your task is to extract property requirements from
WhatsApp messages.

Rules:
- Extract only information supported by the message.
- Do not invent missing information.
- Convert budget amounts into whole numbers in KES.
- Interpret 80k as 80000 and 20k as 20000.
- Interpret monthly budgets as rental inquiries.
- Identify property types such as bedsitter, apartment,
  townhouse, maisonette or house.
- Extract the number of bedrooms where available.
- For missing information, return null.
- For rental_or_sale, use "rental", "sale", or null.
- Treat "under 20k" as a maximum budget of 20000.
- Return only the requested structured data.
- If the user mentions a bedsitter, studio, or similar
  property type without explicitly stating a bedroom
  count, return bedrooms as null, not 0.
- Only extract bedrooms when an explicit bedroom
  count is provided.
"""


# 2. Define the expected JSON structure
PROPERTY_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "property_type": {
            "type": ["STRING", "NULL"]
        },
        "bedrooms": {
            "type": ["INTEGER", "NULL"]
        },
        "location": {
            "type": ["STRING", "NULL"]
        },
        "budget_kes": {
            "type": ["INTEGER", "NULL"]
        },
        "rental_or_sale": {
            "type": ["STRING", "NULL"],
            "enum": ["rental", "sale", None]
        }
    },
    "required": [
        "property_type",
        "bedrooms",
        "location",
        "budget_kes",
        "rental_or_sale"
    ],
    "additionalProperties": False
}


# 3. Extract property details
def extract_property_details(message):

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=message,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
            "response_json_schema": PROPERTY_SCHEMA,
            "temperature": 0
        }
    )

    # Convert JSON response into a Python dictionary
    property_details = json.loads(response.text)

    return property_details


# 4. Google Sheets configuration
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

SPREADSHEET_ID = "18tnwWlGfrgKp1lR7d1WHhh2BO9JRYzY-u1BsHMvlkIA"


def connect_to_google_sheets():

    credentials = Credentials.from_authorized_user_file(
        "token.json", SCOPES
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    worksheet = spreadsheet.sheet1

    return worksheet


# 5. Save to Google Sheets
def save_to_google_sheets(message, details):

    worksheet = connect_to_google_sheets()

    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        message,
        details["property_type"] or "",
        details["bedrooms"] if details["bedrooms"] is not None else "",
        details["location"] or "",
        details["budget_kes"] if details["budget_kes"] is not None else "",
        details["rental_or_sale"] or ""
    ]

    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )

    print("\nInquiry successfully saved to Google Sheets!")


# 6. Print extracted information
def display_details(details):

    print("\n--- PROPERTY INQUIRY DETAILS ---")

    for field, value in details.items():

        # Display missing information clearly
        if value is None:
            value = "Not specified"

        print(f"{field.replace('_', ' ').title()}: {value}")


# 7. Test with three different inquiries
test_messages = [
    "I am looking for a 3-bedroom house in Kileleshwa, budget around 80k per month.",

    "Do you have any bedsitters near Westlands under 20k?",

    "Hello, I am looking for a property. Please let me know what you have available.",

    "Looking for a 2-bedroom apartment in Kilimani. My budget is 65,000 monthly."
]


if __name__ == "__main__":

    while True:

        message = input("\nEnter property inquiry (or 'exit'): ")

        if message.lower() == "exit":
            print("Closing Property Inquiry Extractor.")
            break

        try:
            details = extract_property_details(message)

            display_details(details)

            save_to_google_sheets(message, details)

        except Exception as error:
            print(f"Error processing inquiry: {error}")
            traceback.print_exc()