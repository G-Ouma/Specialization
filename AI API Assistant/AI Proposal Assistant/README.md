# AI Proposal Assistant

**Version:** 1.0.0  
**Status:** Initial proposal-generation release

## Overview

AI Proposal Assistant is a local web application that analyses a client's project brief and generates a concise freelance proposal. Gemini handles brief analysis and proposal wording. Python calculates commercial figures using a configurable pricing profile so the model does not invent prices or delivery durations.

## Implemented features

### Client brief analysis

The backend analyses the submitted brief and returns structured information, including requirements, deliverables, requested deadlines, unclear points, risks, and an effort estimate.

### Proposal generation

The application generates a proposal with six sections:

1. **Opening** — addresses the client's problem.
2. **Understanding** — summarizes the requirements.
3. **Approach** — explains how the work will be done.
4. **Deliverables** — lists expected outputs.
5. **Price and timeline** — uses calculated commercial terms when the scope can be estimated reliably.
6. **Call to action** — proposes a clear next step.

The proposal-generation prompt sets a maximum length of 200 words. The generator checks the result and retries once if it exceeds that limit.

### Deterministic pricing

Pricing is calculated in Python using `backend/pricing_profile.json`. The current profile is:

- Currency: KES
- Daily rate: 3,000
- Minimum project fee: 7,500
- Working hours per day: 8
- Payment terms: 50% upfront, 50% on completion
- Delivery buffer multiplier: 1.5

The price is based on estimated working days and the minimum fee. Proposed delivery days are calculated using the buffer multiplier. If the effort estimate requires further scoping, the generator is instructed not to invent a firm price or delivery timeline.

## Technology

**Backend:** Python, FastAPI, Pydantic, Google Gemini API  
**Frontend:** HTML, CSS, JavaScript  
**Configuration:** JSON pricing profile and `python-dotenv`

## Project structure

```text
AI Proposal Assistant/
├── backend/
│   ├── main.py
│   ├── brief_analyzer.py
│   ├── proposal_generator.py
│   ├── proposal_reviewer.py
│   ├── prompts.py
│   ├── pricing.py
│   ├── pricing_profile.json
│   └── test_*.py
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

## Setup

The application uses the shared virtual environment at the repository root. Follow the [main repository setup](../../../README.md), activate `venv`, and install the root dependencies.

Add the following to the root `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Both variables are required by the brief analysis and proposal generation modules.

Review `backend/pricing_profile.json` and adjust the values to your own pricing arrangement before generating proposals.

## Run locally

Open two PowerShell terminals from the repository root.

**Terminal 1 — backend**

```powershell
.envScriptsActivate.ps1
cd "AI API Assistant\AI Proposal Assistant"
uvicorn backend.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

**Terminal 2 — frontend**

```powershell
cd "AI API Assistant\AI Proposal Assistant\frontend"
python -m http.server 5500
```

Open `http://localhost:5500` in a browser. The backend currently permits the frontend origin `http://localhost:5500`.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Health/message response confirming the API is running |
| POST | `/process` | Accepts `mode` and `text`; currently supports `mode: "generate"` |

Example request body:

```json
{
  "mode": "generate",
  "text": "Client project brief goes here"
}
```

The generate response contains the structured brief analysis and generated proposal. Empty text and unsupported modes return a client error; generation failures are reported as a gateway error.

## Current limitations

- Proposal generation is implemented; proposal review is not implemented in the backend. The review control in the current interface should not be considered a working feature.
- Effort estimates depend on Gemini's interpretation of the brief.
- Delivery estimates use a fixed buffer multiplier and do not account for a real work calendar or availability.
- The API is configured for local development and the frontend origin is hard-coded.
- Pricing is based on one default profile; user accounts and per-client profiles are not implemented.

## Tests

The backend folder contains scripts for brief analysis, pricing, pricing integration, and proposal generation. Run the relevant test scripts from the project directory with the shared environment active. Tests that call Gemini require valid API credentials and may make live API requests.

## Version 1.0.0

- Added client brief analysis.
- Added effort estimation.
- Added configurable Python pricing calculations.
- Added delivery-buffer calculations.
- Added structured proposal generation.
- Added a browser-based frontend.
