import os

print(os.getcwd())
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path

url = "https://books.toscrape.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")


books_data = []

for book in books:

    title = book.h3.a["title"]

    price = book.find("p", class_="price_color").text

    rating = book.find("p", class_="star-rating")["class"][1]

    availability = book.find("p", class_="instock availability").text.strip()

    book_data = {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability
    }
    books_data.append(book_data)
print(books_data)

df=pd.DataFrame(books_data)
BASE_DIR = Path(__file__).resolve().parent.parent

data_folder = BASE_DIR / "data"

data_folder.mkdir(exist_ok=True)

output_file = data_folder / "books.csv"

df.to_csv(output_file, index=False)

print("\nCSV Saved Successfully!")
print(f"Location : {output_file}")



 