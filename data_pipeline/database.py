import sqlite3
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

data_folder = BASE_DIR / "data"

db_file = data_folder / "books.db"

connection = sqlite3.connect(db_file)

print("Database connected successfully!")
print(f"Database location: {db_file}")

cursor = connection.cursor()

csv_file = data_folder / "books.csv"

df = pd.read_csv(csv_file)

print(f"CSV loaded successfully!")
print(f"Rows loaded: {len(df)}")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
""")

connection.commit()

print("Categories table created successfully!")

categories = df["category"].dropna().unique()

cursor.execute("DELETE FROM books")
cursor.execute("DELETE FROM categories")

connection.commit()

print("Existing data cleared!")

for category in categories:
    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        (category,)
    )

connection.commit()

print(f"Categories inserted: {len(categories)}")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL,
    rating INTEGER,
    availability TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
""")

connection.commit()

print("Books table created successfully!")

for _, row in df.iterrows():

    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        (row["category"],)
    )

    category_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO books (
            title,
            price,
            rating,
            availability,
            category_id
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        row["title"],
        row["price"],
        row["rating"],
        row["availability"],
        category_id
    ))

cursor.execute("SELECT COUNT(*) FROM books")
book_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM categories")
category_count = cursor.fetchone()[0]

print(f"Books in database: {book_count}")
print(f"Categories in database: {category_count}")

connection.commit()

print(f"Books inserted: {len(df)}")



