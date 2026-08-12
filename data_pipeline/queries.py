import sqlite3
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

db_file = BASE_DIR / "data" / "books.db"

connection = sqlite3.connect(db_file)

print("Database connected successfully!")


# --------------------------------------------------
# QUERY 1: TOTAL NUMBER OF BOOKS
# --------------------------------------------------

print("\n" + "=" * 50)
print("QUERY 1: TOTAL BOOKS")
print("=" * 50)

cursor = connection.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM books
""")

result = cursor.fetchone()

print("Total books:", result[0])


# --------------------------------------------------
# QUERY 2: TOP 10 HIGHEST-RATED BOOKS
# --------------------------------------------------

print("\n" + "=" * 50)
print("QUERY 2: TOP 10 HIGHEST-RATED BOOKS")
print("=" * 50)

cursor.execute("""
SELECT title, price, rating
FROM books
ORDER BY rating DESC, price DESC
LIMIT 10
""")

results = cursor.fetchall()

for row in results:
    print(row)


# --------------------------------------------------
# QUERY 3: NUMBER OF BOOKS IN EACH CATEGORY
# --------------------------------------------------

print("\n" + "=" * 50)
print("QUERY 3: BOOK COUNT BY CATEGORY")
print("=" * 50)

cursor.execute("""
SELECT
    categories.category_name,
    COUNT(books.book_id) AS book_count
FROM books
JOIN categories
    ON books.category_id = categories.category_id
GROUP BY categories.category_name
ORDER BY book_count DESC
""")

results = cursor.fetchall()

for row in results:
    print(row)


# --------------------------------------------------
# QUERY 4: AVERAGE BOOK PRICE
# --------------------------------------------------

print("\n" + "=" * 50)
print("QUERY 4: AVERAGE BOOK PRICE")
print("=" * 50)

cursor.execute("""
SELECT ROUND(AVG(price), 2)
FROM books
""")

result = cursor.fetchone()

print("Average book price:", result[0])


# --------------------------------------------------
# QUERY 5: ASSIGNMENT CATEGORY ANALYSIS
# Travel, Mystery, Historical Fiction
# --------------------------------------------------

print("\n" + "=" * 50)
print("QUERY 5: ASSIGNMENT CATEGORY ANALYSIS")
print("=" * 50)

query = """
SELECT
    categories.category_name,
    COUNT(books.book_id) AS book_count,
    ROUND(AVG(books.price), 2) AS average_price
FROM books
JOIN categories
    ON books.category_id = categories.category_id
WHERE categories.category_name IN (
    'Travel',
    'Mystery',
    'Historical Fiction'
)
GROUP BY categories.category_name
ORDER BY average_price DESC
"""

df = pd.read_sql_query(query, connection)

print(df)


# --------------------------------------------------
# CLOSE DATABASE CONNECTION
# --------------------------------------------------

connection.close()

print("\nDatabase connection closed.")