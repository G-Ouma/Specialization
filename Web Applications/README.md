# Web Applications

This folder contains small Flask and FastAPI web application exercises. They cover browser forms, HTTP endpoints, JSON requests and responses, and connecting a user interface to Python backend logic.

## Projects

| Project | Description | Documentation |
|---|---|---|
| Complaint Assistant | Generates a professional customer complaint reply using Gemini | [Complaint Assistant](Complaint%20Assistant/README.md) |
| Credit Tracker | Looks up demonstration customer credit balances from an in-memory Python dictionary | [Credit Tracker](Credit%20Tracker/README.md) |
| REST API — Egg Production Tracker | Records and retrieves egg-production entries through a Flask JSON API and browser interface | [REST API](REST%20API/README.md) |

## Technologies

- Python
- Flask
- FastAPI in other repository projects
- HTML, CSS, and JavaScript
- JSON and HTTP APIs
- Google Gemini API for the Complaint Assistant

## Running projects

Each application has its own README with its dependency installation and run commands. The Complaint Assistant and REST API include project-level `requirements.txt` files. Use the shared repository environment where practical, and install the project's listed dependencies before starting its server.

## Learning objectives

- Building web routes and HTTP endpoints
- Accepting and validating user input
- Returning JSON responses and appropriate status codes
- Connecting browser JavaScript to backend routes
- Handling application errors
- Understanding the limitations of in-memory demonstration data

These applications are learning prototypes. In particular, the Credit Tracker and Egg Production Tracker store data in memory and lose it when the server process restarts. Do not use them as persistent production record systems.
