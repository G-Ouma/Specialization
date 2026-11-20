# Tea Harvest Assistant

## Overview

A Python command-line assistant for exploring weather-informed tea-harvesting guidance. It combines Google's Gemini API with weather data from OpenWeather and Open-Meteo for a configured location in Kericho, Kenya.

The user asks a natural-language question. Gemini can call the Python `get_weather()` function when live weather is relevant, then use the returned information to explain whether conditions appear suitable for harvesting.

## Current implementation

- Location is fixed to Kericho coordinates: latitude `-0.3676`, longitude `35.2831`.
- OpenWeather supplies current temperature, humidity, conditions, and an active-rain indicator.
- Open-Meteo supplies hourly temperature, humidity, precipitation, and rain forecast data for the next six hours.
- Gemini function calling decides when to request weather data.
- General questions and greetings can be answered without a weather request.

## Harvesting guidance in the prompt

| Condition | Current guideline |
|---|---|
| Temperature | Preferred range: 15–25°C |
| Humidity | Below 70% preferred |
| Rain | No rain forecast in the next six hours |
| Active rain | Unfavourable |
| Temperature above 28°C | Unfavourable |
| Temperature below 15°C or above 25°C | Requires caution and explanation |

These thresholds are initial operational assumptions, not universal tea-harvesting standards. Validate them with estate management and agronomic guidance before operational use.

## Technology

- Python
- Google Gemini API and function calling
- OpenWeather API
- Open-Meteo forecast API
- `requests`
- `python-dotenv`

## Setup

Use the shared environment and root dependency file described in the [main repository README](../../../README.md). Add the following to the repository-root `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
OPENWEATHER_API_KEY=your_openweather_api_key
```

The script reads the model from `GEMINI_MODEL`, defaulting to `gemini-3.5-flash-lite`. Open-Meteo does not require an API key for this request.

## Run

From this project folder, with the shared environment activated:

```powershell
python main.py
```

Ask whether current weather is suitable for harvesting or ask a general question. Enter `exit` to close the program.

## Current limitations

- Only the configured Kericho location is supported.
- Each question is sent as a separate Gemini generation request; the script does not maintain a multi-turn chat session.
- Weather data availability depends on the external services and network connection.
- Recommendations are based on simplified thresholds and should not be treated as authoritative field instructions.
- The current implementation returns errors from the weather function and Gemini request as text; further validation and user-friendly handling can be added.

## Learning objectives

This project explores Gemini function calling, Python API integration, combining current and forecast weather data, and translating external data into cautious natural-language guidance.
