import sqlite3
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

data_folder = BASE_DIR / "data"

db_file = data_folder / "books.db"

csv_file = data_folder / "books.csv"


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

connection = sqlite3.connect(db_file)

print("Database connected successfully!")
print(f"Database location: {db_file}")

cursor = connection.cursor()


# --------------------------------------------------
# LOAD CSV
# --------------------------------------------------

df = pd.read_csv(csv_file)

print("CSV loaded successfully!")
print(f"Rows loaded: {len(df)}")


# --------------------------------------------------
# ENABLE FOREIGN KEYS
# --------------------------------------------------

cursor.execute("PRAGMA foreign_keys = ON")


# --------------------------------------------------
# RECREATE TABLES
# --------------------------------------------------

cursor.execute("DROP TABLE IF EXISTS books")
cursor.execute("DROP TABLE IF EXISTS categories")

connection.commit()

print("Existing tables cleared!")


# --------------------------------------------------
# CREATE CATEGORIES TABLE
# --------------------------------------------------

cursor.execute("""
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
""")

connection.commit()

print("Categories table created successfully!")


# --------------------------------------------------
# INSERT CATEGORIES
# --------------------------------------------------

categories = df["category"].dropna().unique()

for category in categories:

    cursor.execute(
        """
        INSERT INTO categories (category_name)
        VALUES (?)
        """,
        (category,)
    )

connection.commit()

print(f"Categories inserted: {len(categories)}")


# --------------------------------------------------
# CREATE BOOKS TABLE
# --------------------------------------------------

cursor.execute("""
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL NOT NULL,
    price_inr REAL NOT NULL,
    rating INTEGER NOT NULL,
    in_stock INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
)
""")

connection.commit()

print("Books table created successfully!")


# --------------------------------------------------
# INSERT BOOKS
# --------------------------------------------------

for _, row in df.iterrows():

    cursor.execute(
        """
        SELECT category_id
        FROM categories
        WHERE category_name = ?
        """,
        (row["category"],)
    )

    category_result = cursor.fetchone()

    if category_result is None:
        print(f"Category not found: {row['category']}")
        continue

    category_id = category_result[0]

    cursor.execute(
        """
        INSERT INTO books (
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            int(row["in_stock"]),
            category_id
        )
    )


connection.commit()

print(f"Books inserted: {len(df)}")


# --------------------------------------------------
# VERIFY DATABASE
# --------------------------------------------------

cursor.execute("SELECT COUNT(*) FROM books")

book_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM categories")

category_count = cursor.fetchone()[0]

print(f"Books in database: {book_count}")
print(f"Categories in database: {category_count}")


# --------------------------------------------------
# VERIFY TABLE STRUCTURE
# --------------------------------------------------

print("\nBooks table columns:")

cursor.execute("PRAGMA table_info(books)")

columns = cursor.fetchall()

for column in columns:
    print(column)


# --------------------------------------------------
# CLOSE CONNECTION
# --------------------------------------------------

connection.close()

print("\nDatabase connection closed.")