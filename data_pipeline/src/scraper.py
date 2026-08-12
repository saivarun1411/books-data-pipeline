import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin


print(os.getcwd())

books_data = []

# Required fixed conversion rate
GBP_TO_INR = 105.50

# Scrape first 5 catalogue pages = 100 books
for page in range(1, 6):

    if page == 1:
        url = "https://books.toscrape.com/"
    else:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    print(f"Scraping Page {page}...")

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print(f"Failed to fetch Page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    print(f"Books Found: {len(books)}")

    for book in books:

        title = book.h3.a["title"]

        book_link = book.h3.a["href"]

        book_url = urljoin(url, book_link)

        print(f"Processing: {title}")

        # Fetch individual book page for category
        book_response = requests.get(book_url, timeout=10)

        if book_response.status_code != 200:
            print(f"Failed to fetch book page: {title}")
            continue

        book_soup = BeautifulSoup(book_response.text, "html.parser")

        breadcrumb = book_soup.find("ul", class_="breadcrumb")

        try:
            category = breadcrumb.find_all("li")[2].text.strip()
        except (AttributeError, IndexError):
            print(f"Category parsing failed: {title}")
            continue

        # -----------------------------
        # PRICE
        # -----------------------------

        price_text = book.find(
            "p",
            class_="price_color"
        ).text.strip()

        try:
            price_gbp = float(
                price_text.replace("Â£", "").replace("£", "")
            )
        except ValueError:
            print(f"Price parsing failed: {title}")
            continue

        # -----------------------------
        # RATING
        # -----------------------------

        rating_text = book.find(
            "p",
            class_="star-rating"
        )["class"][1]

        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        try:
            rating = rating_map[rating_text]
        except KeyError:
            print(f"Rating parsing failed: {title}")
            continue

        # -----------------------------
        # AVAILABILITY
        # -----------------------------

        availability = book.find(
            "p",
            class_="instock availability"
        ).text.strip()

        in_stock = availability.lower().startswith("in stock")

        # -----------------------------
        # GBP → INR
        # -----------------------------

        price_inr = round(price_gbp * GBP_TO_INR, 2)

        # -----------------------------
        # STORE RECORD
        # -----------------------------

        book_data = {
            "title": title,
            "price_gbp": price_gbp,
            "price_inr": price_inr,
            "rating": rating,
            "in_stock": in_stock,
            "category": category
        }

        books_data.append(book_data)

    print(f"Completed Page {page}")


# -----------------------------
# CREATE DATAFRAME
# -----------------------------

df = pd.DataFrame(books_data)

print(f"\nTotal Books Scraped: {len(books_data)}")
print(f"Total Rows in DataFrame: {len(df)}")

print("\nData Types:")
print(df.dtypes)


# -----------------------------
# SAVE CSV
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

data_folder = BASE_DIR / "data"

data_folder.mkdir(exist_ok=True)

output_file = data_folder / "books.csv"

df.to_csv(output_file, index=False)

print("\nCSV Saved Successfully!")
print(f"Location : {output_file}")