# Property Inquiry Extractor

## Overview

This Python command-line prototype uses Google's Gemini API to extract property requirements from a manually entered enquiry and append the results to a Google Sheet. It is designed around messages a real-estate agent might receive through WhatsApp, but it does not connect to WhatsApp.

## Extracted fields

| Field | Meaning |
|---|---|
| `property_type` | Property category, such as bedsitter, apartment, house, townhouse, or maisonette |
| `bedrooms` | Explicitly stated bedroom count; otherwise null |
| `location` | Area or location mentioned in the enquiry |
| `budget_kes` | Budget normalized to a whole-number KES amount |
| `rental_or_sale` | `rental`, `sale`, or null when not stated |

The extraction instructions tell Gemini not to invent missing details. Missing values are represented as null and displayed as “Not specified”.

## Processing flow

1. Enter an enquiry in the terminal.
2. Gemini returns data matching the application's JSON schema.
3. Python parses and displays the extracted fields.
4. The application authenticates to Google Sheets using a locally stored OAuth token.
5. The original message and extracted values are appended to the first worksheet.

## Technology

- Python and JSON
- Google Gemini API through the Google Gen AI SDK
- Google Sheets API and `gspread`
- `google-auth`, `google-auth-oauthlib`
- `python-dotenv`

## Files

```text
2 - Property Inquiry/
├── Main.py
├── test_sheets.py
└── README.md
```

The shared virtual environment and root `requirements.txt` are used. OAuth credentials and tokens are local files and must not be committed.

## Setup

### 1. Shared environment

From the repository root, activate the shared environment and install root dependencies. See the [main README](../../../README.md).

### 2. Gemini key

Add this to the root `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Google Sheets OAuth

You need a Google Cloud project with the Google Sheets API enabled, OAuth credentials for a Desktop application, and a spreadsheet editable by the Google account used for authorization.

Save the downloaded OAuth client file in this project folder as `client_secret.json`. Run `test_sheets.py` to perform the OAuth flow and create `token.json`. The main application expects an existing token and does not initiate the login flow itself.

The spreadsheet ID is currently hard-coded in both scripts. Replace it with your own spreadsheet ID before running them.

The first worksheet is expected to have columns in this order: Date received, Original message, Property type, Bedrooms, Location, Budget (KES), Rental or sale.

## Run

From this folder, with the shared environment activated:

```powershell
python test_sheets.py
python Main.py
```

The test script authorizes Google Sheets and appends a sample row. Running it more than once can add duplicate sample rows. The main program then accepts enquiries until you enter `exit`.

Example:

```text
I am looking for a 3-bedroom house in Kileleshwa, budget around 80k per month.
```

## Testing notes

The example enquiry strings in `Main.py` are reference examples; they are not automatically run as an extraction test suite. `test_sheets.py` tests authorization and spreadsheet row insertion, not Gemini extraction accuracy.

## Limitations

- Enquiries are entered manually; WhatsApp integration is not implemented.
- Customer names and contact details are not extracted.
- Duplicate detection and lead-status tracking are not implemented.
- Spreadsheet ID and Gemini model are configured in source code.
- A valid OAuth token must already exist before the main program can save data.
- Human review is recommended before treating extracted details as confirmed requirements.

## Learning objectives

This project practises structured AI extraction, JSON schema use, OAuth authentication, API integration, and automated spreadsheet updates.
