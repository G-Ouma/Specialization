# API Basics

## Purpose

This exercise introduces HTTP requests and JSON response handling using the REST Countries API. It includes a direct country lookup and a second script that reads an API credential from the shared environment.

## Files

- `day1_api.py` — requests information for Kenya and prints the common name, capital, population, and currency.
- `test.py` — requests country information using the alpha-2 code `KE`, reads `REST_COUNTRIES_API_KEY` from the root `.env`, and prints the response.

## Requirements and setup

Use the shared Python environment described in the [repository README](../../README.md). Install the root `requirements.txt` and create a root `.env` file.

For `test.py`, configure:

```env
REST_COUNTRIES_API_KEY=your_rest_countries_api_key
```

The first script currently contains a demonstration authorization value in its source. It is not a place to insert a real private credential.

## Run

From this project folder, with the shared environment activated:

```powershell
python day1_api.py
python test.py
```

## Concepts practised

- Making GET requests with `requests`
- Supplying authorization headers
- Checking HTTP response status
- Parsing JSON and navigating nested fields
- Reading credentials from environment variables

## Notes

These are introductory exercises, not a production API client. The scripts print API responses and do not yet include a reusable client layer or automated test suite. Keep private credentials out of source code.
