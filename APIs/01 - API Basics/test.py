import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("REST_COUNTRIES_API_KEY")

url = "https://api.restcountries.com/countries/v5/codes.alpha_2/KE"

headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers, timeout=10)

print("Status:", response.status_code)

result = response.json()
print("Response:", result)