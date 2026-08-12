import os

print(os.getcwd())
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin



books_data = []

for page in range(1, 6):

    if page == 1:
        url = "https://books.toscrape.com/"
    else:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    print(f"Scraping Page {page}...")

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch Page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    print(f"Books Found: {len(books)}")


    for book in books:

        title = book.h3.a["title"]

        book_link = book.h3.a["href"]

        print(f"\nProcessing: {title}")

        book_url = urljoin(url, book_link)

        print("Book URL:", book_url)

        book_response = requests.get(book_url, timeout=10)
        book_soup = BeautifulSoup(book_response.text, "html.parser")
        

        
        

        print("Book page downloaded")

        

        breadcrumb = book_soup.find("ul", class_="breadcrumb")
        category = breadcrumb.find_all("li")[2].text.strip()

        print("Category:", category)

        price = book.find("p", class_="price_color").text.strip()
        price=price.replace("Â£", "").replace("£", "")
        price = float(price)

        rating_text = book.find("p", class_="star-rating")["class"][1]
        rating_map = {
            "One":1,
            "Two":2,
            "Three":3,
            "Four":4,
            "Five":5
        }

        rating = rating_map[rating_text]

        availability = book.find("p", class_="instock availability").text.strip()

        book_data = {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "category": category
        }

        books_data.append(book_data)
print(f"Completed Page {page}")

df=pd.DataFrame(books_data)

print(f"\nTotal Books Scraped: {len(books_data)}")
print(f"Total Rows in DataFrame: {len(df)}")

BASE_DIR = Path(__file__).resolve().parent.parent

data_folder = BASE_DIR / "data"

data_folder.mkdir(exist_ok=True)

output_file = data_folder / "books.csv"

df.to_csv(output_file, index=False)

print("\nCSV Saved Successfully!")
print(f"Location : {output_file}")




 