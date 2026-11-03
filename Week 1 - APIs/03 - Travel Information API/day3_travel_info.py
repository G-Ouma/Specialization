"""
Travel Weather Tool
-------------------
Shows weather and country information for any city.

Usage:
    python day3_travel_info.py

Requirements:
    pip install requests python-dotenv
    OPENWEATHER_API_KEY in .env file
"""

import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
restcountries_api_key = os.getenv("REST_COUNTRIES_API_KEY")

TIMEOUT = 10



def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": f"{city},KE",
        "appid": openweather_api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        # print("Weather API response:", response.json())
        return response.json()

    except requests.exceptions.Timeout:
        print("Error: The weather request timed out. Try again.")
        return None

    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            print(f"Error: City '{city}' was not found.")
        elif response.status_code == 401:
            print("Error: Invalid or unauthorized API key.")
        else:
            print(f"Weather API error: HTTP {response.status_code}")
        return None

    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")
        return None


def get_country_info(country_code):
    url = (
        "https://api.restcountries.com/"
        f"countries/v5/codes.alpha_2/{country_code}"
    )

    headers = {
        "Authorization": f"Bearer {os.getenv('REST_COUNTRIES_API_KEY')}"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        result = response.json()
        # print("Country API response:", result)
        return result["data"]["objects"][0]

    except (
        requests.exceptions.RequestException,
        KeyError,
        IndexError
    ) as error:
        print(f"Country lookup failed: {error}")
        return None


def save_to_history(data):
    filename = "travel_history.json"

    # Load existing history if the file exists
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            history = json.load(file)
    else:
        history = []

    # Add the new search
    history.append(data)

    # Save the updated history
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

    print(f"\nSearch saved to {filename}")


def run_tool():
    print("Travel Weather Tool")
    print("-------------------")

    city = input("Enter a city name: ").strip()

    if not city:
        print("No city entered. Exiting.")
        return

    print(f"\nFetching data for {city}...")

    weather = get_weather(city)

    if weather is None:
        return

    country_code = weather.get("sys", {}).get("country", "Unknown")
    main = weather.get("main", {})
    conditions = weather.get("weather", [])
    wind = weather.get("wind", {})

    print(f"\n=== {city.title()}, {country_code} ===")
    print(f"Temperature : {main.get('temp', 'N/A')}°C")
    print(
        "Condition   : "
        f"{conditions[0].get('description', 'N/A').title()}"
        if conditions else "Condition   : N/A"
    )
    print(f"Humidity    : {main.get('humidity', 'N/A')}%")
    print(f"Wind        : {wind.get('speed', 'N/A')} m/s")

    country = get_country_info(country_code)

    if country:
        print("\n=== Country Info ===")
        print(f"Region      : {country.get('region', 'Unknown')}")
        print(f"Population  : {country.get('population', 0):,}")

        currencies = country.get("currencies", [])
        currency_names = [
            item.get("name", item.get("code", "Unknown"))
            for item in currencies
        ]
        print(
            "Currency    : "
            + (", ".join(currency_names) if currency_names else "Unknown")
        )

        record = {
            "city": weather["name"],
            "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
            "country_code": weather["sys"]["country"],
            "temperature": weather["main"]["temp"],
            "condition": weather["weather"][0]["description"],
            "humidity": weather["main"]["humidity"],
            "wind_speed": weather["wind"]["speed"],
            "region": country.get("region", "Unknown"),
            "population": country.get("population", 0),
            "currency": ", ".join(
                currency["name"]
                for currency in country.get("currencies", [])
            ) or "Unknown"
        }

        save_to_history(record)



if __name__ == "__main__":
    run_tool()