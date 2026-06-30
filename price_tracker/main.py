import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

URL = "https://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_html(url):
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def extract_prices(html):
    soup = BeautifulSoup(html, "html.parser")

    price_tags = soup.find_all("p", class_="price_color")

    prices = [tag.text.strip() for tag in price_tags]

    return prices


def save_prices(prices):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("prices.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for price in prices:
            writer.writerow([timestamp, price])


def main():
    print("Starting price scraping...")

    try:
        html = get_html(URL)
    except requests.RequestException as e:
        print("Request failed:", e)
        return

    prices = extract_prices(html)

    if prices:
        save_prices(prices)
        print(f"Saved {len(prices)} prices successfully!")
    else:
        print("No prices found.")


if __name__ == "__main__":
    main()
