# Books Data Pipeline

A Python-based end-to-end data pipeline that scrapes book information, cleans and transforms the data, stores it in SQLite, and performs SQL analysis using Pandas.

## Project Objective

The project demonstrates:

- Web scraping
- Data cleaning and transformation
- CSV generation
- SQLite database creation
- SQL querying
- Pandas analysis
- Git version control

The assignment focuses on three categories:

- Travel
- Mystery
- Historical Fiction

## Project Structure

`	ext
capstone_project 1/
¦
+-- data_pipeline/
¦   +-- data/
¦   ¦   +-- books.csv
¦   +-- src/
¦   ¦   +-- scraper.py
¦   ¦   +-- cleaner.py
¦   +-- database.py
¦   +-- queries.py
¦   +-- requirements.txt
¦   +-- README.md
¦
+-- .gitignore


## Currency Conversion

The required fixed baseline conversion rate is **1 GBP = 105.50 INR**.

No external currency API is used. The INR price is calculated as: price_inr = price_gbp * 105.50.

## Data Cleaning Decisions

- GBP price is converted to float in price_gbp.
- Star ratings One through Five are converted to integers 1 through 5.
- Availability is converted to boolean in_stock.
- Invalid numeric values are handled using median imputation.

## SQL and Pandas Analysis

Six SQL queries demonstrate SELECT/WHERE, ORDER BY, LIMIT, DISTINCT, BETWEEN, IN, and JOIN. Query outputs are saved in data_pipeline/data/query_outputs.txt.

Multiple results are loaded using pd.read_sql(), and the SQL JOIN is reproduced using pd.merge(). The comparison returns True.

## How to Run

pip install -r data_pipeline/requirements.txt
python data_pipeline/src/scraper.py
python data_pipeline/src/cleaner.py
python data_pipeline/database.py
python data_pipeline/queries.py
