import sqlite3
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

data_folder = BASE_DIR / "data"

db_file = data_folder / "books.db"

output_file = data_folder / "query_outputs.txt"

connection = sqlite3.connect(db_file)

print("Database connected successfully!")


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

all_outputs = []


def run_query(query_number, title, query):
    """
    Execute a SQL query, print the result,
    and save the query + output for submission evidence.
    """

    print("\n" + "=" * 70)
    print(f"QUERY {query_number}: {title}")
    print("=" * 70)

    print("\nSQL:")
    print(query.strip())

    result = pd.read_sql(query, connection)

    print("\nOUTPUT:")
    print(result.to_string(index=False))

    all_outputs.append(
        f"""
{'=' * 70}
QUERY {query_number}: {title}
{'=' * 70}

SQL:
{query.strip()}

OUTPUT:
{result.to_string(index=False)}

"""
    )

    return result


# --------------------------------------------------
# QUERY 1
# SELECT + WHERE
# --------------------------------------------------

query_1 = """
SELECT
    title,
    price_gbp,
    rating,
    in_stock
FROM books
WHERE rating >= 4
"""

df_query_1 = run_query(
    1,
    "Books with rating 4 or higher",
    query_1
)


# --------------------------------------------------
# QUERY 2
# ORDER BY + LIMIT
# --------------------------------------------------

query_2 = """
SELECT
    title,
    price_gbp,
    price_inr,
    rating
FROM books
ORDER BY rating DESC, price_gbp DESC
LIMIT 10
"""

df_query_2 = run_query(
    2,
    "Top 10 highest-rated books",
    query_2
)


# --------------------------------------------------
# QUERY 3
# DISTINCT
# --------------------------------------------------

query_3 = """
SELECT DISTINCT
    category_name
FROM categories
ORDER BY category_name
"""

df_query_3 = run_query(
    3,
    "Distinct book categories",
    query_3
)


# --------------------------------------------------
# QUERY 4
# BETWEEN
# --------------------------------------------------

query_4 = """
SELECT
    title,
    price_gbp,
    rating
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp
"""

df_query_4 = run_query(
    4,
    "Books priced between £20 and £40",
    query_4
)


# --------------------------------------------------
# QUERY 5
# JOIN + IN
# --------------------------------------------------

query_5 = """
SELECT
    categories.category_name,
    COUNT(books.book_id) AS book_count,
    ROUND(AVG(books.price_gbp), 2) AS average_price_gbp
FROM books
JOIN categories
    ON books.category_id = categories.category_id
WHERE categories.category_name IN (
    'Travel',
    'Mystery',
    'Historical Fiction'
)
GROUP BY categories.category_name
ORDER BY average_price_gbp DESC
"""

df_query_5 = run_query(
    5,
    "Assignment category analysis",
    query_5
)


# --------------------------------------------------
# QUERY 6
# JOIN QUERY FOR PANDAS COMPARISON
# --------------------------------------------------

query_6 = """
SELECT
    books.title,
    books.price_gbp,
    books.price_inr,
    books.rating,
    books.in_stock,
    categories.category_name
FROM books
JOIN categories
    ON books.category_id = categories.category_id
ORDER BY books.book_id
"""

df_sql_join = run_query(
    6,
    "Book details with category using SQL JOIN",
    query_6
)


# --------------------------------------------------
# PANDAS read_sql()
# --------------------------------------------------

print("\n" + "=" * 70)
print("PANDAS read_sql() RESULTS")
print("=" * 70)

print("\nQuery 2 loaded using pd.read_sql():")
print(df_query_2.to_string(index=False))

print("\nQuery 5 loaded using pd.read_sql():")
print(df_query_5.to_string(index=False))


# --------------------------------------------------
# LOAD DATABASE TABLES INTO PANDAS
# --------------------------------------------------

books_df = pd.read_sql(
    "SELECT * FROM books",
    connection
)

categories_df = pd.read_sql(
    "SELECT * FROM categories",
    connection
)


# --------------------------------------------------
# REPRODUCE SQL JOIN USING pd.merge()
# --------------------------------------------------

df_pandas_merge = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)


# Select the same columns and order as SQL JOIN

df_pandas_merge = df_pandas_merge[
    [
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category_name"
    ]
].copy()


# SQL result is ordered by book_id.
# Pandas merge result is also sorted by title-independent
# database order, so sort both results by the same columns.

df_sql_compare = df_sql_join.sort_values(
    by=[
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category_name"
    ]
).reset_index(drop=True)

df_pandas_compare = df_pandas_merge.sort_values(
    by=[
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category_name"
    ]
).reset_index(drop=True)


# --------------------------------------------------
# COMPARE SQL JOIN AND PANDAS MERGE
# --------------------------------------------------

join_results_match = df_sql_compare.equals(
    df_pandas_compare
)

print("\n" + "=" * 70)
print("SQL JOIN vs PANDAS MERGE")
print("=" * 70)

print("\nSQL JOIN result:")
print(df_sql_compare.head(10).to_string(index=False))

print("\nPandas merge result:")
print(df_pandas_compare.head(10).to_string(index=False))

print("\nDo SQL JOIN and Pandas merge produce equivalent results?")
print(join_results_match)


# Save comparison result

all_outputs.append(
    f"""
{'=' * 70}
SQL JOIN vs PANDAS MERGE
{'=' * 70}

SQL JOIN result:
{df_sql_compare.head(10).to_string(index=False)}

Pandas merge result:
{df_pandas_compare.head(10).to_string(index=False)}

Equivalent results:
{join_results_match}
"""
)


# --------------------------------------------------
# SAVE ALL QUERY STRINGS AND OUTPUTS
# --------------------------------------------------

with open(output_file, "w", encoding="utf-8") as file:

    file.write("BOOKS DATA PIPELINE - SQL QUERY OUTPUTS\n")
    file.write("=" * 70)
    file.write("\n")

    for output in all_outputs:
        file.write(output)

print("\nQuery outputs saved successfully!")
print(f"Location: {output_file}")


# --------------------------------------------------
# CLOSE DATABASE CONNECTION
# --------------------------------------------------

connection.close()

print("\nDatabase connection closed.")