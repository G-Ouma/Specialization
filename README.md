# Python & AI/ML Specialization

This repository documents my progression through Python programming, APIs, automation, and Artificial Intelligence/Machine Learning (AI/ML).

The focus is on learning by building practical mini-projects, understanding the code, and improving projects incrementally.

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
    └── Matatu Assistant/
```

Each week has an overview README. Each mini-project has its own README describing its purpose, setup, usage, and learning outcomes.

## Shared Python environment

All projects use one virtual environment at the repository root. Do not create a separate environment inside each week or mini-project.

### Windows PowerShell

From the repository root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If the root `venv` already exists, activate it rather than recreating it.

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## API credentials

1. Copy `.env.example` to a file named `.env` in the repository root.
2. Add your own API keys to `.env`.
3. Keep `.env` private. It is excluded from Git.

The current examples use these environment variables where applicable:

- `OPENWEATHER_API_KEY`
- `REST_COUNTRIES_API_KEY`
- `GEMINI_API_KEY`

Never commit real API keys or paste them into source files.

## Managing dependencies

The root `requirements.txt` is the single dependency list for the specialization.

When a project needs a new external package, install it in the activated shared environment and add its package name (and, when appropriate, a version constraint) to the root `requirements.txt`. Python standard-library modules such as `os`, `json`, and `datetime` do not need to be installed.

## Learning progress

- [x] Week 1 — APIs and external data
- [ ] Week 2 — To be added
- [x] Week 3 — AI API assistant prototype

## Learning approach

I aim to build a small working project for each important concept, document what it does, test it, and improve it over time. The repository will grow as I progress toward practical AI/ML engineering work.
