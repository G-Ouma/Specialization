# Weather API

## Purpose

Practice retrieving current weather information for a city using the OpenWeather API.

## File

- `day2_weather.py` — loads `OPENWEATHER_API_KEY` from the root `.env` file, sends a weather request, and prints temperature, conditions, and humidity.

## Setup

1. Follow the shared setup in the [repository README](../../README.md).
2. Add your OpenWeather API key to the root `.env` file:

```env
OPENWEATHER_API_KEY=your_key_here
```

## Run

```powershell
python day2_weather.py
```

The city is currently set in the script. Change the `city` value in `day2_weather.py` before running it for a different location.

## Learning points

- Building API URLs
- Reading JSON responses
- Using environment variables
- Handling common HTTP status codes
