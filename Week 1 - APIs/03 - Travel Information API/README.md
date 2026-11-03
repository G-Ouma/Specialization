# Travel Information API

## Purpose

Combine two external APIs to display weather and country information for a city.

## File

- `day3_travel_info.py` — retrieves weather from OpenWeather, uses the returned country code to request country information, and saves successful searches to a local JSON history file.

## Setup

Follow the shared setup in the [repository README](../../README.md). Add both keys to the root `.env` file:

```env
OPENWEATHER_API_KEY=your_openweather_key
REST_COUNTRIES_API_KEY=your_rest_countries_key
```

## Run

```powershell
python day3_travel_info.py
```

Enter a city when prompted.

## Local search history

The program creates or updates `travel_history.json` in its current working directory. This is generated data and is intentionally excluded from Git.

## Learning points

- Integrating multiple APIs
- Passing data from one API request into another
- Handling network errors, timeouts, and missing response fields
- Working with timestamps
- Reading and writing JSON files
