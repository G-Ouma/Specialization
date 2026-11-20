# Complaint Reply Assistant

## Overview

A Flask web application that turns a customer complaint into a concise, professional reply draft using Google's Gemini API. The user enters a complaint in the browser, requests a reply, and can copy the generated text.

The assistant is designed to acknowledge the customer's concern, use empathetic language, avoid blame, and suggest a realistic next step.

## Features

- Browser interface for entering a complaint.
- Generates a reply using Gemini.
- Validates that the complaint is present and no longer than 5,000 characters.
- Returns user-friendly errors when the AI service is not configured or a request fails.
- Displays the generated reply and provides a **Copy Reply** action.
- Uses logging for server-side error diagnosis.

The prompt instructs the model not to invent refunds, discounts, compensation, guarantees, or unconfirmed timelines.

## Technology and structure

- Python and Flask
- Google Gemini API through the Google Gen AI SDK
- HTML, CSS, and JavaScript
- `python-dotenv`
- Gunicorn for production serving

```text
Complaint Assistant/
├── main.py
├── requirements.txt
└── static/
    ├── index.html
    ├── script.js
    └── style.css
```

## Configuration

The application loads environment variables from the working environment. Configure the shared repository-root `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_available_gemini_model
```

Both variables should be set for the deployed application. The code logs a warning if either is missing; without a Gemini key, the generation endpoint returns a service-unavailable response.

## Install and run locally

From this project directory, activate the repository's shared environment and install this application's dependencies:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Flask starts the application locally. Open the address printed by Flask, normally `http://127.0.0.1:5000`.

## HTTP endpoint

| Method | Path | Input | Purpose |
|---|---|---|---|
| GET | `/` | — | Serves the application page |
| POST | `/generate` | JSON with a `complaint` string | Returns a generated reply or an error |

Example request:

```json
{
  "complaint": "My order has not arrived and nobody has updated me."
}
```

A successful response contains a `reply` field. Invalid or empty input returns HTTP 400; an unconfigured AI service returns 503; a generation failure returns 502.

## Deployment

The application has been deployed on Render:

[Complaint Reply Assistant](https://complain-reply-assistant.onrender.com/)

Configure `GEMINI_API_KEY` and `GEMINI_MODEL` as environment variables in the hosting service. The project includes Gunicorn in its requirements for production serving.

## Limitations

- The generated text is a draft and should be reviewed before sending to a customer.
- The application does not connect to customer records, order systems, or refund workflows.
- It cannot verify whether a proposed next step is actually available to the business.
- It does not store complaint history in a database.

## Learning objectives

This project practises Flask routing, request validation, JSON APIs, Gemini integration, frontend/backend communication, error handling, and deployment.
