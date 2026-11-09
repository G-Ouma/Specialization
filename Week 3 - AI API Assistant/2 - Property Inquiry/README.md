# Property Inquiry Extractor

## Overview

Property Inquiry Extractor is a Python command-line prototype that uses Google's Gemini API to turn unstructured property enquiries into structured information and append the results to a Google Sheet.

It is designed around enquiries a property agent might receive in a WhatsApp message. The current prototype accepts messages manually in the terminal; it does not connect to WhatsApp.

## What it extracts

The application asks Gemini to return these fields:

| Field | Description |
|---|---|
| `property_type` | Property category, such as apartment, house or bedsitter |
| `bedrooms` | Explicitly stated number of bedrooms |
| `location` | Mentioned area or location |
| `budget_kes` | Budget converted to a whole-number KES amount |
| `rental_or_sale` | `rental`, `sale`, or null when not stated |

The extraction instructions tell the model not to invent missing details. Missing values are represented as `null` and displayed as “Not specified”.

After extraction, the original message and extracted fields are appended to the first worksheet of the configured Google spreadsheet.

## How it works

1. The user enters a property enquiry in the terminal.
2. Gemini interprets the message and returns data matching a defined JSON schema.
3. Python parses and displays the extracted fields.
4. The application authenticates with Google Sheets using a locally stored OAuth token.
5. The original message and extracted details are appended as a new spreadsheet row.

## Technology

- Python
- Google Gemini API through the Google Gen AI SDK
- Google Sheets API
- `gspread`
- `google-auth-oauthlib` and `google-auth`
- `python-dotenv`
- JSON

## Project files

```text
2 - Property Inquiry/
├── Main.py
├── test_sheets.py
└── README.md
```

The project uses the shared virtual environment, dependency file, and environment configuration at the root of the `Specialization` repository. OAuth files are created locally and should not be committed.

## Setup

### 1. Prepare the shared environment

From the root of the `Specialization` repository, activate the shared virtual environment and install the root dependencies if you have not already done so.

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

See the [main repository README](../../../README.md) for the complete shared setup.

### 2. Configure the Gemini API key

Add your key to the root `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

The project loads this environment variable with `python-dotenv`. Keep the real `.env` file private.

### 3. Configure Google Sheets access

You need:
- A Google Cloud project with the Google Sheets API enabled.
- OAuth credentials for a Desktop application.
- A Google spreadsheet that the Google account used for OAuth can edit.

Download the OAuth client credentials and save them in this project folder as `client_secret.json`.

The current `Main.py` expects an existing `token.json`; it does not initiate the OAuth login flow itself. The `test_sheets.py` script performs that authorization flow, saves the token, and appends a sample row to the spreadsheet.

Before running either script, replace the spreadsheet ID in both `Main.py` and `test_sheets.py` with the ID of your own spreadsheet.

### 4. Prepare the spreadsheet

The first worksheet should have columns in this order:

| Column | Value |
|---|---|
| A | Date received |
| B | Original message |
| C | Property type |
| D | Bedrooms |
| E | Location |
| F | Budget (KES) |
| G | Rental or sale |

## Run

Run commands from the Property Inquiry folder, with the shared virtual environment activated.

### Authorize and test Google Sheets

```powershell
python test_sheets.py
```

This opens the Google OAuth authorization flow if a valid token is not already available. It then appends a sample enquiry row. Running it again may append another sample row.

### Process enquiries

After `token.json` has been created:

```powershell
python Main.py
```

Enter an enquiry when prompted. Type `exit` to close the program.

Example enquiry:

```text
I am looking for a 3-bedroom house in Kileleshwa,
budget around 80k per month.
```

The program displays the extracted details and attempts to save them to the spreadsheet.

## Testing notes

The code includes several example enquiry strings in `Main.py`, covering:
- A three-bedroom house in Kileleshwa with a monthly budget of KES 80,000.
- Bedsitters near Westlands under KES 20,000.
- An enquiry with few specified details.
- A two-bedroom apartment in Kilimani with a monthly budget of KES 65,000.

These examples are currently stored in a list in the script; they are not automatically executed as a test suite. The separate `test_sheets.py` script tests Google Sheets authorization and row insertion, not the Gemini extraction logic.

## Current limitations

- Enquiries are entered manually; WhatsApp integration is not implemented.
- The application does not extract customer names or contact details.
- Duplicate detection and enquiry status tracking are not implemented.
- The spreadsheet ID is currently hard-coded in the scripts.
- The main application relies on a previously created OAuth token.
- The Gemini model name is currently specified in the source code and may need updating if that model is unavailable.
- Extracted information should be checked by a person before being treated as a confirmed customer requirement.

## Possible next improvements

- Move the spreadsheet ID and model name into configuration.
- Add a dedicated automated test suite for extraction and normalization.
- Improve validation of budgets and property requirements.
- Add duplicate detection and lead status tracking.
- Integrate WhatsApp Business messaging.
- Build a dashboard for reviewing and managing enquiries.

## Purpose

This project explores practical AI-assisted information extraction, structured JSON output, API integration, OAuth authentication, and automated spreadsheet updates.
