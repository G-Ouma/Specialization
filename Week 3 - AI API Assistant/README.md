# Week 3 — Thika Matatu SACCO AI Member Assistant

A small Python command-line assistant that helps a SACCO secretary answer common member questions. A member types a question in natural language and Gemini generates a clear response using fixed information in the system prompt.

## How the solution works\n\n1. **Input:** The secretary enters a member's question in the terminal.\n2. **Context:** Python sends the question to Gemini together with a system prompt containing the sample SACCO facts and response rules.\n3. **Interpretation:** Gemini interprets the member's wording (including informal phrasing) and selects the relevant information.\n4. **Response:** Python prints Gemini's answer in the terminal.\n\nThe model is responsible for understanding and phrasing the answer; the system prompt supplies the facts. This prototype does not fetch live account data.\n\n## What it can answer

- **Member balance:** Demonstrates a sample balance of KSh 3,500 for demo member THK-014 (as at 3 November 2026).
- **Next meeting:** Friday, 13 November 2026 at 10:00 a.m. at the SACCO office in Thika.
- **Membership fees:** KSh 500 one-time registration fee, KSh 2,000 one-time joining fee, and KSh 1,000 monthly contribution.

> **Important:** All SACCO details are fictional sample data for demonstration. The script does not connect to a SACCO database and must not be used to disclose real member balances. Replace the sample details with approved information and add secure member verification before real-world deployment.

## Requirements

- Python 3.10+
- A Gemini API key (the Gemini API has a free usage tier subject to Google's current limits and availability)

## Setup

1. Clone the repository and open the `Week 3 - AI API Assistant` folder, or download this folder from GitHub.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
6. Copy `.env.example` to `.env` and add your key:

   ```env
   GEMINI_API_KEY=put_your_real_key_here
   ```

   Keep `.env` private. It is excluded from Git.

## Run the assistant

```bash
python main.py
```

Type a question, for example:

- What is my balance?
- When is our next meeting?
- How much are the monthly contributions?

Type `exit` to close the assistant.

## Test different question phrasings

Run:

```bash
python test_assistant.py
```

The test script sends six differently worded questions (including informal and Swahili phrasing) to Gemini and checks that the answer contains an expected detail. It makes six API requests.

## Project files

- `main.py` — interactive command-line assistant and system prompt.
- `test_assistant.py` — six live question-variation checks.
- `requirements.txt` — Python dependencies.
- `.env.example` — example environment-variable file.

## Limitations and next steps

This is a prototype. The sample balance is the same every time and is not a personal account lookup. A production version should authenticate members, retrieve balances from a protected database, keep fees and meeting details editable, log unanswered questions, and require secretary confirmation for sensitive or uncertain requests.
