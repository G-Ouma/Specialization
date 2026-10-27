
import requests

url = "https://api.restcountries.com/countries/v5/names.common/Kenya"

headers = {
    "Authorization": "Bearer rc_live_demo"
}

response = requests.get(url, headers=headers, timeout=15)

if response.status_code == 200:
    result = response.json()

    countries = result["data"]["objects"]
    country = countries[0]

    name = country["names"]["common"]
    capital = country["capitals"][0]
    population = country["population"]
    currency = country["currencies"][0]

    print(f"Country: {name}")
    print(f"Capital: {capital}")
    print(f"Population: {population:,}")
    print(f"Currency: {currency}")

else:
    print("Request failed. Status:", response.status_code)
    print(response.text)
