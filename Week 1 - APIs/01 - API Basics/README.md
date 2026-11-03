# API Basics

## Purpose

Practice making a direct HTTP request to the REST Countries API and reading selected fields from its JSON response.

## Files

- `day1_api.py` — requests country information and prints the country's name, capital, population, and currency.
- `test.py` — makes a second country lookup using an API key loaded from the root `.env` file and prints the response.

## Setup

Use the shared environment and root dependency file. See the [repository setup guide](../../README.md).

For `test.py`, provide `REST_COUNTRIES_API_KEY` in the root `.env` file.

## Run

From this mini-project folder, with the root environment activated:

```powershell
python day1_api.py
python test.py
```

## Learning points

- Sending GET requests with `requests`
- Passing request headers
- Checking response status codes
- Parsing JSON and accessing nested fields

## Notes

The scripts are learning exercises. The first script contains a demonstration credential in its source, while the second reads a credential from an environment variable. Do not put a real API key in source code.
