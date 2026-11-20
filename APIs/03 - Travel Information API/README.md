# Travel Information API

## Purpose

This command-line tool combines weather and country information for a city. It uses the country code returned by OpenWeather to request additional details from the REST Countries API.

## Features

- Prompts for a city name and requests its current weather.
- Displays temperature, conditions, humidity, and wind speed.
- Looks up the associated country's region, population, and currencies.
- Saves a successful combined lookup to a local JSON history file.
- Handles common request failures, including timeouts and unsuccessful HTTP responses.

The weather lookup currently appends `,KE` to the city query, so it is configured for Kenyan locations.

## Requirements and configuration

Use the shared Python environment described in the [repository README](../../README.md). Add both keys to the root `.env` file:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
REST_COUNTRIES_API_KEY=your_rest_countries_api_key
```

## Run

From this project folder, with the shared environment activated:

```powershell
python day3_travel_info.py
```

Enter a city name when prompted.

## Search history

Successful lookups are appended to `travel_history.json` in the current working directory. Each record includes the city, local timestamp, country code, weather values, region, population, and currency names. The generated history file is excluded from version control.

## Concepts practised

- Integrating multiple REST APIs
- Passing data from one API response into another request
- Handling request errors and missing response fields
- Working with timestamps
- Reading and writing JSON files

## Limitations

The country lookup depends on a successful weather response. The city query is restricted to Kenya, and the history file is a local JSON file rather than a database.
