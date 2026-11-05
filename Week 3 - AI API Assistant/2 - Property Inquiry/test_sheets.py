
import os
import gspread
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# Authenticate with Google
credentials = None

if os.path.exists("token.json"):
    credentials = Credentials.from_authorized_user_file(
        "token.json", SCOPES
    )

if credentials and credentials.expired and credentials.refresh_token:
    credentials.refresh(Request())

if not credentials or not credentials.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    credentials = flow.run_local_server(port=0)

# Save credentials for future use
with open("token.json", "w") as token:
    token.write(credentials.to_json())

# Connect to Google Sheets
client = gspread.authorize(credentials)

spreadsheet = client.open_by_key("18tnwWlGfrgKp1lR7d1WHhh2BO9JRYzY-u1BsHMvlkIA")
worksheet = spreadsheet.sheet1

# Sample inquiry
sample_message = (
    "Looking for a 2-bedroom apartment in Kilimani. "
    "My budget is 65,000 monthly."
)

# Insert a test row
row = [
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    sample_message,
    "apartment",
    2,
    "Kilimani",
    65000,
    "rental"
]

worksheet.append_row(row, value_input_option="USER_ENTERED")

print("Successfully connected to Google Sheets!")
print("Test inquiry successfully added!")
print("Spreadsheet:", spreadsheet.title)
