# Pharmacy Chatbot

## Overview

A Python command-line prototype that uses Google's Gemini API to answer common customer enquiries using pharmacy information supplied in a system instruction. The example is configured for Kisumu Pharmacy in Kisumu, Kenya.

This is an information assistant, not a pharmacy management system, pharmacist, or source of medical advice.

## Features

- Answers questions about configured operating hours and services.
- Explains general prescription and repeat-prescription processes.
- Maintains conversation context during the active chat session.
- Does not claim access to live medicine inventory or an official price list.
- Provides user-facing messages for service errors and usage limits.

## Configured information

The system instruction includes operating hours, a list of services, general prescription-processing guidance, and repeat-prescription information. Straightforward prescription processing is described as typically taking 15–30 minutes, but the assistant is instructed not to guarantee a completion time.

The assistant must refer uncertain medication or medical questions to pharmacy staff. It must not invent medicine stock, prices, or service charges.

**Verify all pharmacy details before any real-world use.** The application does not connect to inventory, pricing, patient, or prescription systems.

## Conversation context

The application creates a Gemini chat session at startup and sends each user message through that session. Earlier messages can therefore inform follow-up answers while the program is running. The application does not persist chat history after it closes.

## Technology and files

- Python
- Google Gemini API through the Google Gen AI SDK
- `python-dotenv`

```text
3 - Pharmacy Chatbot/
├── main.py
└── README.md
```

The project uses the shared virtual environment, root `requirements.txt`, and root `.env`.

## Setup

Follow the shared environment instructions in the [main repository README](../../../README.md). Add the following to the repository-root `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

The model variable is optional; the script uses `gemini-3.5-flash-lite` when it is not set.

## Run

From this project folder, with the shared environment activated:

```powershell
python main.py
```

Ask about services, opening hours, prescriptions, or other configured information. Enter `exit` to close the session.

## Limitations and safety

- The pharmacy details are prompt-defined sample information and must be verified.
- The assistant cannot confirm medicine availability or prices.
- It does not diagnose conditions, recommend treatment, or replace pharmacist judgement.
- Conversation context lasts only for the active session.
- Technical exception details are printed to the terminal for debugging.

A production implementation would need verified configuration, privacy and logging controls, approved integrations, testing, and a clear staff handoff process.
