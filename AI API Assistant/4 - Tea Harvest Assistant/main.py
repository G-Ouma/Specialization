
import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Kericho coordinates
LATITUDE = -0.3676
LONGITUDE = 35.2831


# ==========================================
# WEATHER TOOL
# ==========================================

def get_weather() -> dict:
    """Retrieve current weather and the next 6 hours of forecasts for Kericho, Kenya."""

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
        # Current weather from OpenWeatherMap
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

        # Hourly forecast from Open-Meteo
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

        return {
            "location": "Kericho, Kenya",
            "current_weather": current_weather,
            "next_6_hours": next_six_hours
        }

    except requests.exceptions.RequestException as error:
        return {"error": f"Weather service error: {error}"}

    except (KeyError, IndexError, TypeError, ValueError) as error:
        return {"error": f"Unexpected weather data format: {error}"}


# ==========================================
# GEMINI CONFIGURATION
# ==========================================

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
You are a Tea Harvest Assistant for a tea estate in Kericho, Kenya.

Your role is to answer questions about tea harvesting and weather conditions.

WEATHER DECISION RULES:

1. Good harvesting conditions:
   - No rain forecast in the next 6 hours.
   - Temperature between 15 and 25 degrees Celsius.
   - Humidity below 70%.

2. Poor harvesting conditions:
   - Active rain or rain forecast.
   - Temperature above 28 degrees Celsius.

3. Temperatures below 15 degrees or above 25 degrees
   require caution and explanation.

4. Humidity of 70% or above is considered high.
   This is an operational assumption, not a universal tea
   harvesting standard.

FUNCTION CALLING:

- Call get_weather when the user asks about current weather,
  today's harvesting conditions, or whether harvesting
  should proceed based on current conditions.
- Do not call get_weather for greetings, general explanations,
  or unrelated questions.
- Never invent weather information.
- If the weather function returns an error, explain that
  live weather information is unavailable.

RESPONSE STYLE:

- Use simple, practical language.
- Give a clear harvesting recommendation when weather
  information is available.
- Explain which weather conditions support your recommendation.
- Do not claim conditions are suitable if the data is incomplete.
"""


# ==========================================
# CHAT FUNCTION
# ==========================================

def chat_with_assistant(question):
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=[get_weather]
            )
        )

        return response.text or "I couldn't generate a response."

    except Exception as error:
        return f"Assistant error: {error}"


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("=" * 45)
    print("       TEA HARVEST ASSISTANT")
    print("=" * 45)
    print("Kericho Tea Estate")
    print("Ask me about weather and harvesting.")
    print("Type 'exit' to close.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        if not question:
            continue

        answer = chat_with_assistant(question)

        print(f"\nAssistant: {answer}\n")
