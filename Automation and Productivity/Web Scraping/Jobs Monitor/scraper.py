import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://quotes.toscrape.com"

all_quotes = []

page = 1

while True:
    url = f"{base_url}/page/{page}/"

    response = requests.get(url)

    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    if not quotes:
        break

    for quote in quotes:
        quote_text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text

        tags = [
            tag.text for tag in quote.find_all("a", class_="tag")
        ]

        all_quotes.append({
            "quote": quote_text,
            "author": author,
            "tags": ", ".join(tags),
            "source_url": url
        })

    print(f"Scraped page {page}: {len(quotes)} quotes")

    page += 1

print(f"\nTotal quotes collected: {len(all_quotes)}")

with open("scraped_quotes.csv", "w", newline="", encoding="utf-8-sig") as file:
    fieldnames = ["quote", "author", "tags", "source_url"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(all_quotes)

print("\nData successfully saved to scraped_quotes.csv")