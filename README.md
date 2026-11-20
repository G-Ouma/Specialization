# Python & AI/ML Specialization

A practical Python learning repository focused on building small, working applications while developing skills in API integration, generative AI, automation, web development, and data-driven tools.

The repository is organized by project area rather than week number. Each project has its own folder and, where applicable, its own setup instructions.

## Repository projects

| Area | Projects |
|---|---|
| [APIs](APIs/README.md) | API Basics, Weather API, Travel Information API, Browser Country Lookup |
| [AI API Assistant](AI%20API%20Assistant/README.md) | Matatu Assistant, Property Inquiry Extractor, Pharmacy Chatbot, Tea Harvest Assistant, AI Proposal Assistant |
| [Web Applications](Web%20Applications/README.md) | Complaint Reply Assistant, Credit Tracker, Poultry Egg Production REST API |
| [Automation and Productivity](Automation%20and%20Productivity/README.md) | Legal Client File Sorter, Jobs Monitor web-scraping project |
| [Football Scouting Intelligence](Football%20Scouting%20Intelligence/) | Football player statistics and scouting application |

## Repository structure

```text
Specialization/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── APIs/
│   ├── README.md
│   ├── 01 - API Basics/
│   ├── 02 - Weather API/
│   ├── 03 - Travel Information API/
│   └── 04 - Browser Country Lookup/
├── AI API Assistant/
│   ├── README.md
│   ├── 1 - Matatu Assistant/
│   ├── 2 - Property Inquiry/
│   ├── 3 - Pharmacy Chatbot/
│   ├── 4 - Tea Harvest Assistant/
│   └── AI Proposal Assistant/
├── Web Applications/
│   ├── README.md
│   ├── Complaint Assistant/
│   ├── Credit Tracker/
│   └── REST API/
├── Automation and Productivity/
│   ├── README.md
│   ├── File Automation/
│   └── Web Scraping/
└── Football Scouting Intelligence/
```

## Python environment

Most Python exercises use one shared virtual environment at the repository root. Do not create a separate environment for every project.

### Windows PowerShell

Run these commands from the repository root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If the root `venv` already exists, activate it instead of recreating it.

Some applications have their own dependency files or additional server requirements. Install those only when working on the relevant project; their READMEs explain the commands. For example, the Complaint Assistant and REST API have project-level `requirements.txt` files.

## Environment variables and credentials

1. Copy `.env.example` to `.env` in the repository root.
2. Add the credentials required by the project you intend to run.
3. Keep `.env`, OAuth tokens, and downloaded client secrets private.

Common variables include:

- `GEMINI_API_KEY` — Google Gemini API access.
- `GEMINI_MODEL` — model name for projects that read the model from the environment.
- `OPENWEATHER_API_KEY` — OpenWeather API access.
- `REST_COUNTRIES_API_KEY` — credential used by the REST Countries exercises.

Some integrations also require separate setup, such as Google Sheets API enablement and OAuth Desktop credentials. Follow the project README for those steps. Never commit real API keys, OAuth client secrets, or access tokens.

## Dependencies

The root `requirements.txt` contains shared Python libraries used by several projects. Some applications also have project-specific dependencies. Activate the shared environment before installing them, and use the relevant project's requirements file where one exists.

## Working with the projects

- Read the README inside a project folder before running it.
- Run commands from the working directory specified in that README.
- Check whether the project requires API credentials or external service setup.
- Treat sample records and hard-coded business information as demonstration data.
- Do not use prototype applications to make real financial, medical, legal, or operational decisions without appropriate validation and safeguards.

## Project status

This repository is continuously evolving. Some folders contain completed learning exercises, while others contain prototypes under active development. Individual READMEs describe implemented behaviour and known limitations; planned features should not be assumed to be available.

## Author

Gerald Ouma
