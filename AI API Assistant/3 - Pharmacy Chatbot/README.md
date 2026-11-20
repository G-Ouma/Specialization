# Pharmacy Chatbot

## Overview

Pharmacy Chatbot is a Python command-line prototype that uses Google's Gemini API to answer common customer enquiries using pharmacy information supplied in a system instruction.

The example is configured for a pharmacy in Kisumu, Kenya. It is an information assistant, not a live pharmacy management system and not a substitute for a qualified pharmacist.

## Features

- Answers questions about configured operating hours and services.
- Responds to common prescription-processing and repeat-prescription questions.
- Maintains conversation context during the current application session, so users can ask follow-up questions.
- Avoids claiming access to live medicine stock or an official price list.
- Provides user-facing messages when the Gemini service is unavailable or usage limits are reached.

## Information available to the assistant

The system instruction currently includes:

- Operating hours for Monday to Saturday and Sunday.
- A configured list of pharmacy services.
- General guidance about prescription processing.
- General information about repeat-prescription requirements.
- Instructions to refer uncertain medical or medication questions to pharmacy staff.

The stated prescription processing time is an estimate only. The assistant is instructed not to guarantee a completion time.

**Important:** Confirm that the pharmacy details and service information are accurate and authorized before using this prototype in a real pharmacy. The assistant does not connect to pharmacy records, inventory, pricing, or patient systems.

## How conversation memory works

The application creates a Gemini chat session when it starts and sends each user message through that session. This allows Gemini to use earlier messages as context during the running session.

Conversation history is not saved by this application for use after it closes.

## Technology

- Python
- Google Gemini API through the Google Gen AI SDK
- `python-dotenv`

## Project files

```text
3 - Pharmacy Chatbot/
├── main.py
└── README.md
```

The project uses the shared virtual environment, root `requirements.txt`, and root `.env` file in the `Specialization` repository. It does not require a separate project-level environment or requirements file.

## Setup

### 1. Prepare the shared environment

From the root of the `Specialization` repository, activate the shared virtual environment and install the root dependencies if you have not already done so.

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

See the [main repository README](../../../README.md) for the shared setup instructions.

### 2. Configure Gemini

Add your API key to the root `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=your_available_gemini_model
```

The application reads `GEMINI_API_KEY` and optionally `GEMINI_MODEL`. If `GEMINI_MODEL` is not set, the source code currently defaults to `gemini-3.5-flash-lite`. Use a model currently available to your Gemini API account.

Keep the real `.env` file private and never commit API keys.

## Run

Open PowerShell and navigate to this project folder:

```powershell
cd "Week 3 - AI API Assistant\3 - Pharmacy Chatbot"
python main.py
```

Run the command with the shared virtual environment activated. The program starts an interactive session. Type `exit` to close it.

**Before running the current repository version:** check that the first line of `main.py` contains only valid Python. The version currently in the repository has a stray `cd` line before the imports; remove that line or the script will stop with a syntax error.

## Example questions

- What are your operating hours?
- Do you process repeat prescriptions?
- How long does a straightforward prescription usually take?
- Do you have a particular medicine in stock?
- How much does a medication cost?

For stock and price enquiries, the assistant should explain that it cannot access live inventory or an official price list and direct the customer to pharmacy staff.

## Safety and limitations

- Requires internet access and a working Gemini API key.
- Depends on Gemini API availability and account usage limits.
- Does not connect to live medicine inventory or pricing.
- Does not access patient records or process prescriptions.
- Does not diagnose conditions, recommend treatment, or replace pharmacist judgement.
- Pharmacy operating hours, services, and processing guidance are prompt-defined information and must be kept accurate.
- Conversation context exists only during the active session.
- The current source prints technical exception details to the terminal for debugging; these should be handled more carefully in a deployed application.

## Possible next improvements

- Move pharmacy information into a separately editable configuration source.
- Add tests for common questions, follow-up questions, and unsupported requests.
- Add stronger privacy and logging controls.
- Connect to approved, access-controlled inventory and pricing systems if required.
- Build a web interface for staff or customers.
- Add a clear handoff workflow to pharmacy staff for questions the assistant cannot answer.

## Purpose

This project explores conversational AI, system instructions, Gemini chat sessions, context retention, and responsible boundaries for an AI-powered information assistant.
