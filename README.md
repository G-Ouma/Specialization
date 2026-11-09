# Python & AI/ML Specialization

This repository documents my practical learning journey in Python, API integration, automation, and Artificial Intelligence/Machine Learning (AI/ML).

The focus is on learning by building: each project applies a concept to a small, practical problem, with code, testing, and documentation that evolve as the work progresses.

## Repository contents

### Week 1 — APIs

Practical exercises in working with external APIs, handling JSON data, managing API credentials, and using APIs from Python and browser JavaScript.

| Project | What it covers |
|---|---|
| [01 - API Basics](Week%201%20-%20APIs/01%20-%20API%20Basics/README.md) | Making HTTP requests and reading REST Countries API responses |
| [02 - Weather API](Week%201%20-%20APIs/02%20-%20Weather%20API/README.md) | Retrieving current weather data from OpenWeather |
| [03 - Travel Information API](Week%201%20-%20APIs/03%20-%20Travel%20Information%20API/README.md) | Combining weather and country data and saving search history |
| [04 - Browser Country Lookup](Week%201%20-%20APIs/04%20-%20Browser%20Country%20Lookup/README.md) | Calling a country API from a browser with JavaScript `fetch()` |

### Week 3 — AI API Assistant

Small AI-powered applications built with Python and Google's Gemini API.

| Project | What it covers |
|---|---|
| [1 - Matatu Assistant](Week%203%20-%20AI%20API%20Assistant/1%20-%20Matatu%20Assistant/README.md) | A command-line SACCO member FAQ assistant using sample information |
| [2 - Property Inquiry](Week%203%20-%20AI%20API%20Assistant/2%20-%20Property%20Inquiry/README.md) | Extracting structured property requirements from natural-language inquiries and saving them to Google Sheets |
| [3 - Pharmacy Chatbot](Week%203%20-%20AI%20API%20Assistant/3%20-%20Pharmacy%20Chatbot/README.md) | A conversational pharmacy information assistant with session context |
| [4 - Tea Harvest Assistant](Week%203%20-%20AI%20API%20Assistant/4%20-%20Tea%20Harvest%20Assistant/README.md) | Using Gemini function calling and weather APIs to support tea-harvesting decisions |
| [AI Proposal Assistant](Week%203%20-%20AI%20API%20Assistant/AI%20Proposal%20Assistant/README.md) | Analysing client briefs and generating structured proposals with Python-based pricing |

Each project folder contains its own README with project-specific details, configuration, and instructions.

## Repository structure

```text
Specialization/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── Week 1 - APIs/
│   ├── README.md
│   ├── 01 - API Basics/
│   ├── 02 - Weather API/
│   ├── 03 - Travel Information API/
│   └── 04 - Browser Country Lookup/
└── Week 3 - AI API Assistant/
    ├── README.md
    ├── 1 - Matatu Assistant/
    ├── 2 - Property Inquiry/
    ├── 3 - Pharmacy Chatbot/
    ├── 4 - Tea Harvest Assistant/
    └── AI Proposal Assistant/
        ├── README.md
        ├── backend/
        └── frontend/
```

## Shared Python environment

All Python projects use one virtual environment at the repository root and the root `requirements.txt`. Do not create separate virtual environments or project-level dependency files unless a project has a specific requirement that cannot be managed centrally.

### Windows PowerShell

From the repository root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If the root `venv` already exists, activate it rather than recreating it.

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## API credentials and configuration

1. Copy `.env.example` to `.env` in the repository root.
2. Add the API keys required by the project you want to run.
3. Keep the real `.env` file private; it is excluded from Git.

Environment variables used by projects in this repository include:

- `OPENWEATHER_API_KEY`
- `REST_COUNTRIES_API_KEY`
- `GEMINI_API_KEY`

Some projects also require service-specific setup, such as Google Sheets API access and OAuth credentials. Follow the relevant project's README for those additional steps.

Never commit API keys, OAuth client secrets, access tokens, or other credentials.

## Managing dependencies

The root `requirements.txt` is the shared dependency list.

When a project needs an additional external package, install it in the activated shared environment and add it to the root requirements file. Python standard-library modules such as `os`, `json`, `math`, and `pathlib` do not need to be installed separately.

## Learning progress

- [x] Week 1 — APIs and external data
- [ ] Week 2 — Not yet added
- [x] Week 3 — Gemini API and AI assistant prototypes

This repository is a work in progress. Project descriptions reflect the current state of each implementation; prototypes may have limitations documented in their individual READMEs.
