
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Kericho coordinates
LATITUDE = -0.3676
LONGITUDE = 35.2831


def get_weather():
    """Retrieve current weather and the next 6 hours of forecasts."""

    if not OPENWEATHER_API_KEY:
        return {"error": "OpenWeatherMap API key is missing."}

    base_url = "https://api.openweathermap.org/data/2.5"

    params = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        # 1. Get current weather from OpenWeatherMap
        current_response = requests.get(
            f"{base_url}/weather",
            params=params,
            timeout=15
        )
        current_response.raise_for_status()
        current = current_response.json()

        current_weather = {
            "temperature": current["main"]["temp"],
            "humidity": current["main"]["humidity"],
            "description": current["weather"][0]["description"],
            "rain_active": (
                current.get("rain", {}).get("1h", 0) > 0
            )
        }

        # 2. Get hourly forecast from Open-Meteo
        forecast_url = "https://api.open-meteo.com/v1/forecast"

        forecast_params = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "rain"
            ],
            "forecast_hours": 6,
            "timezone": "Africa/Nairobi"
        }

        forecast_response = requests.get(
            forecast_url,
            params=forecast_params,
            timeout=15
        )
        forecast_response.raise_for_status()

        forecast = forecast_response.json()

        # 3. Process the hourly forecast
        hourly = forecast["hourly"]

        next_six_hours = []

        for i in range(len(hourly["time"])):
            next_six_hours.append({
                "time": hourly["time"][i],
                "temperature": hourly["temperature_2m"][i],
                "humidity": hourly["relative_humidity_2m"][i],
                "precipitation_mm": hourly["precipitation"][i],
                "rain_mm": hourly["rain"][i]
            })

        # 4. Return combined weather information
        return {
            "location": "Kericho, Kenya",
            "current_weather": current_weather,
            "next_6_hours": next_six_hours
        }

    except requests.exceptions.RequestException as error:
        return {"error": f"Weather service error: {error}"}

    except (KeyError, IndexError, TypeError, ValueError) as error:
        return {"error": f"Unexpected weather data format: {error}"}


# Test the weather function independently
if __name__ == "__main__":
    weather = get_weather()
    print(weather)
