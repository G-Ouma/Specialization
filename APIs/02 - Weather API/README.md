# Weather API

## Purpose

This exercise retrieves current weather for a configured city using the OpenWeather Current Weather API.

## File

- `day2_weather.py` — loads `OPENWEATHER_API_KEY` from the repository-root `.env`, requests current weather in metric units, and displays temperature, condition description, and humidity. It includes handling for common invalid-key, city-not-found, and rate-limit responses.

## Setup

1. Follow the shared environment instructions in the [repository README](../../README.md).
2. Add an OpenWeather API key to the root `.env` file:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
```

## Run

From this folder, with the shared environment activated:

```powershell
python day2_weather.py
```

The city is currently assigned in the script. Edit the `city` variable in `day2_weather.py` to query a different location. The current checked-in value is a placeholder and should be replaced with a valid city before running.

## Concepts practised

- Building an API request URL
- Supplying an API key
- Reading JSON weather fields
- Working with metric units
- Handling common HTTP status codes

## Limitations

This exercise requests current conditions only. It does not provide forecasts, save historical observations, or accept a city interactively.
