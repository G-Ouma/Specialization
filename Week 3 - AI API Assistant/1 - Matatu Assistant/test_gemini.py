
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(r"C:\Projects\Python\100 Days\Specialization\.env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(attempts=1)
    )
)

start = time.time()

try:
    print("Sending request to Gemini...")

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Reply with just: Hello"
    )

    print("Response:", response.text)

except Exception as error:
    print("Error:", error)

finally:
    print(f"Elapsed time: {time.time() - start:.2f} seconds")
