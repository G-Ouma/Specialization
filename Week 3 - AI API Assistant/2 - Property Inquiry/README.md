# Property Inquiry Extractor

An AI-powered property inquiry extraction tool built with Python, Google's Gemini API, and Google Sheets.

The application processes unstructured property inquiries, extracts relevant requirements into structured JSON, and automatically saves the results to a Google Sheet.

## 1. Problem Statement

Property agents often receive inquiries through WhatsApp in natural language, such as:

> I am looking for a 3-bedroom house in Kileleshwa, budget around 80k per month.

Manually reading each message and transferring the information into a spreadsheet is repetitive and time-consuming.

This project automates that process using an AI-powered information extraction pipeline.

## 2. Features

- Accepts raw property inquiry messages through the terminal.
- Uses Google's Gemini API to interpret natural language.
- Extracts five structured fields:
  - `property_type`
  - `bedrooms`
  - `location`
  - `budget_kes`
  - `rental_or_sale`
- Converts the AI-generated JSON response into a Python dictionary.
- Handles missing information without inventing values.
- Normalizes budget expressions such as `80k` into `80000`.
- Preserves the original inquiry message.
- Automatically appends extracted information to Google Sheets.
- Reuses Google OAuth authorization through a locally stored token.

## 3. Technologies Used

- **Python** – Application logic and data processing.
- **Google Gemini API** – Natural language understanding and information extraction.
- **Google Sheets API** – Online storage of extracted inquiries.
- **gspread** – Python interface for Google Sheets.
- **google-auth-oauthlib** – Google OAuth authentication.
- **python-dotenv** – Environment variable management.
- **JSON** – Structured data representation.

## 4. Project Structure

```text
Property Inquiry/
│
├── main.py
├── test_sheets.py
├── README.md
├── requirements.txt
├── .env
├── .env.example
├── client_secret.json
├── token.json
└── .gitignore
```

Sensitive files such as `.env`, `client_secret.json`, and `token.json` are excluded from Git.

## 5. Setup and Installation

### Prerequisites

- Python 3
- A Google Gemini API key
- A Google Cloud project with the Google Sheets API enabled
- A Google spreadsheet
- OAuth Desktop application credentials

### Install dependencies

Activate your Python virtual environment and install the required packages:

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

### Configure Google Sheets authentication

1. Create an OAuth Desktop application in Google Cloud Console.
2. Download the OAuth client credentials.
3. Save the downloaded file as `client_secret.json` in the project directory.
4. Authorize the application using your Google account.
5. Ensure the Google Sheets API is enabled.
6. Replace the spreadsheet ID in `main.py` with your own spreadsheet ID.

The application stores its OAuth authorization token locally as `token.json`.

### Prepare the Google Sheet

Create a spreadsheet and ensure the first worksheet contains these columns:

| Column | Field |
|---|---|
| A | Date Received |
| B | Original Message |
| C | Property Type |
| D | Bedrooms |
| E | Location |
| F | Budget (KES) |
| G | Rental or Sale |

## 6. Running the Application

Run:

```bash
python main.py
```

Enter a property inquiry when prompted.

Example:

```text
I am looking for a 3-bedroom house in Kileleshwa,
budget around 80k per month.
```

The application extracts the information, displays the results, and saves a new row to Google Sheets.

Type `exit` to close the application.

## 7. Example Output

```text
--- PROPERTY INQUIRY DETAILS ---

Property Type: house
Bedrooms: 3
Location: Kileleshwa
Budget Kes: 80000
Rental Or Sale: rental

Inquiry successfully saved to Google Sheets!
```

## 8. Testing

The extraction logic was tested using four different inquiries:

1. A three-bedroom house in Kileleshwa with a monthly budget of KSh 80,000.
2. A bedsitter near Westlands under KSh 20,000.
3. An inquiry with missing property information.
4. A two-bedroom apartment in Kilimani with a monthly budget of KSh 65,000.

The tests verified property classification, bedroom extraction, location identification, budget normalization, rental classification, and handling of missing information.

A separate Google Sheets connection test verified successful authentication and row insertion.

## 9. Current Limitations

- Inquiries are currently entered manually through the terminal.
- WhatsApp integration has not yet been implemented.
- Customer names and phone numbers are not yet extracted.
- Duplicate inquiry detection is not yet implemented.
- Inquiry status tracking is not yet implemented.

## 10. Future Improvements

- Integrate WhatsApp Business Cloud API for automatic message reception.
- Extract customer names and contact details.
- Detect duplicate inquiries.
- Introduce inquiry status tracking.
- Improve validation of extracted property requirements.
- Develop a simple dashboard for managing property leads.

## Author

Developed as a practical Python and AI integration project exploring natural language processing, structured information extraction, API integration, and automated data storage.