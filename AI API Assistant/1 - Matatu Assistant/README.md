# Matatu SACCO Member Assistant

## Project overview

A small Python command-line assistant that helps a SACCO secretary answer common member questions. A member types a question in natural language and Gemini generates a clear response using fixed information in the system prompt.

The model is responsible for understanding and phrasing the answer; the system prompt supplies the facts. This prototype does not fetch live account data.

## What it can answer

- **Member balance:** Demonstrates a sample balance of KSh 3,500 for demo member THK-014 (as at 3 November 2026).
- **Next meeting:** Friday, 13 November 2026 at 10:00 a.m. at the SACCO office in Thika.
- **Membership fees:** KSh 500 one-time registration fee, KSh 2,000 one-time joining fee, and KSh 1,000 monthly contribution.

> **Important:** All SACCO details are fictional sample data for demonstration. The script does not connect to a SACCO database and must not be used to disclose real member balances. Replace the sample details with approved information and add secure member verification before real-world deployment.

## Requirements

- Python 3.10+
- A Gemini API key
- The shared specialization environment with dependencies installed from the root `requirements.txt`

## Configuration

Add the following to the root `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Keep the real `.env` file private.

## Run the assistant

From this folder, with the shared environment activated:

```powershell
python main.py
```

Type a question, for example:

- What is my balance?
- When is our next meeting?
- How much are the monthly contributions?

Type `exit` to close the assistant.

## Run the question checks

```powershell
python test_assistant.py
```

The test script sends six differently worded questions (including informal and Swahili phrasing) to Gemini and checks for expected details. It makes six API requests and requires a working API key.

## Files

- `main.py` — interactive command-line assistant and system prompt.
- `test_assistant.py` — six live question-variation checks.

## Limitations and next steps

This is a prototype. The sample balance is the same every time and is not a personal account lookup. A production version should authenticate members, retrieve balances from a protected database, keep fees and meeting details editable, log unanswered questions, and require secretary confirmation for sensitive or uncertain requests.
