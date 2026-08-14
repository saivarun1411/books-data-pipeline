# Books Data Pipeline

A Python-based end-to-end data pipeline that scrapes book information from Books to Scrape, cleans and transforms the data, converts GBP prices to INR using the required fixed project rate, loads the data into a normalized SQLite database, and performs SQL and Pandas analysis.

## Project Objective

This project demonstrates an end-to-end data pipeline involving:

- Web scraping using Requests and BeautifulSoup
- Data cleaning and type conversion
- Fixed-rate currency conversion
- CSV generation
- Normalized SQLite database design
- SQL querying and analysis
- Pandas `read_sql()` analysis
- Pandas `merge()` as an alternative to SQL JOIN
- Git version control

The assignment analysis focuses on the following categories:

- Travel
- Mystery
- Historical Fiction

## Data Source

The data is scraped from:

https://books.toscrape.com/

The scraper processes the first 5 paginated catalogue pages and produces 100 book records across 29 categories.

The scraping process is fully automated and does not require manual copy-pasting.

## Project Structure

```text
capstone_project 1/
│
├── data_pipeline/
│   ├── data/
│   │   ├── books.csv
│   │   └── query_outputs.txt
│   │
│   ├── src/
│   │   ├── scraper.py
│   │   └── cleaner.py
│   │
│   ├── database.py
│   ├── queries.py
│   ├── requirements.txt
│   └── README.md
│
└── .gitignore
```

## Pipeline Workflow

```text
Books to Scrape
      ↓
Web Scraping
      ↓
Raw Book Data
      ↓
Cleaning & Transformation
      ↓
books.csv
      ↓
SQLite Database
      ↓
SQL Queries
      ↓
Pandas read_sql()
      ↓
Pandas merge()
      ↓
Analysis & Results
```

## Installation

From the project root directory:

```bash
cd "C:\capstone_project 1"
```

Install the required Python packages:

```bash
pip install -r data_pipeline/requirements.txt
```

## How to Execute

Run the pipeline in the following order.

### Step 1 — Scrape the Data

Run:

```bash
python data_pipeline/src/scraper.py
```

The scraper automatically requests the first five catalogue pages from Books to Scrape and extracts book information.

The scraper produces 100 book records across 29 categories.

The extracted information includes:

- Book title
- Price
- Rating
- Availability
- Category

No manual copy-pasting is required.

### Step 2 — Clean and Transform the Data

Run:

```bash
python data_pipeline/src/cleaner.py
```

The cleaning script converts the scraped values into the required formats and creates the cleaned CSV dataset.

The resulting dataset is saved as:

```text
data_pipeline/data/books.csv
```

### Step 3 — Create and Populate the SQLite Database

Run:

```bash
python data_pipeline/database.py
```

This creates the SQLite database and loads the cleaned book data into the normalized relational schema.

The database contains two related tables:

```text
categories
     │
     │ 1
     │
     │ N
     ▼
   books
```

### Step 4 — Run SQL and Pandas Analysis

Run:

```bash
python data_pipeline/queries.py
```

The query script executes the required SQL queries and Pandas analysis.

The printed SQL and Pandas outputs are saved to:

```text
data_pipeline/data/query_outputs.txt
```

## Currency Conversion

The project uses the required fixed project-defined conversion rate:

**1 GBP = 105.50 INR**

No external currency API is used.

The INR price is calculated using:

```text
price_inr = price_gbp × 105.50
```

For example:

```text
£10.00 × 105.50 = ₹1,055.00
```

The rate is a fixed project baseline and does not depend on a particular date or live exchange-rate service.

## Data Cleaning and Parsing Decisions

The scraper extracts values from HTML and the cleaning stage converts them into consistent analytical types.

### Price

The scraped price contains the pound currency symbol.

Example:

```text
£51.77
```

It is cleaned and converted into a numeric `price_gbp` value:

```text
51.77
```

### Rating

The website provides ratings as text labels such as:

```text
One
Two
Three
Four
Five
```

These are converted into integer values from 1 to 5.

### Availability

The availability information is converted into the boolean `in_stock` field.

For example:

```text
In stock
```

is represented as:

```text
True
```

### INR Price

The `price_inr` field is calculated from `price_gbp` using the fixed project rate:

```text
1 GBP = 105.50 INR
```

### Category

The category is extracted from the book information and preserved as a category name.

### CSV

After cleaning and transformation, the final dataset is written to:

```text
data_pipeline/data/books.csv
```

This CSV provides an offline copy of the processed dataset for analysis and database loading.

## Final Dataset Columns

The cleaned dataset contains the required fields:

| Column | Description | Type |
|---|---|---|
| `title` | Book title | String |
| `price_gbp` | Original price in GBP | Float |
| `rating` | Book rating from 1 to 5 | Integer |
| `in_stock` | Whether the book is in stock | Boolean |
| `price_inr` | Converted INR price | Float |
| `category` | Book category | String |

## SQLite Database Design

The project uses a normalized two-table relational database.

### Categories Table

The `categories` table stores unique book categories.

```text
categories
-----------
category_id      PRIMARY KEY
category_name
```

### Books Table

The `books` table stores the book information.

```text
books
-----
book_id          PRIMARY KEY
title
price_gbp
price_inr
rating
in_stock
category_id      FOREIGN KEY
```

The relationship is:

```text
books.category_id
        ↓
categories.category_id
```

This allows book records to be associated with their corresponding categories without duplicating category information.

The database is created and populated by:

```bash
python data_pipeline/database.py
```

## SQL Analysis

The project contains multiple SQL queries and their printed outputs.

The queries collectively demonstrate the required SQL operations, including:

- `SELECT`
- `WHERE`
- `ORDER BY`
- `LIMIT`
- `DISTINCT`
- `COUNT()`
- `AVG()`
- `GROUP BY`
- `IN`
- `JOIN`

The SQL statements and their outputs are recorded in:

```text
data_pipeline/data/query_outputs.txt
```

## SQL Query Examples

### Query 1 — Filtering and Sorting

The project uses SQL filtering and sorting to identify books based on specified conditions.

Example operations:

```sql
SELECT ...
FROM books
WHERE ...
ORDER BY ...
LIMIT ...
```

### Query 2 — Top-Rated Books

The project includes a query that filters books by rating and orders the results by price.

Example output includes fields such as:

```text
title
price_gbp
price_inr
rating
```

### Query 3 — Distinct Categories

The project uses `DISTINCT` to identify unique categories represented in the dataset.

### Query 4 — Aggregation

The project uses aggregation functions such as:

```sql
COUNT()
AVG()
```

to calculate summary statistics.

### Query 5 — Category Analysis

The assignment categories are analysed using filtering, grouping, and average-price calculations.

The query uses:

```sql
WHERE category_name IN (...)
GROUP BY category_name
ORDER BY average_price_gbp DESC
```

Example output:

```text
category_name       book_count    average_price_gbp
Historical Fiction      1              53.74
Travel                  1              45.17
Mystery                 3              41.32
```

### Query 6 — SQL JOIN

The project performs a relational JOIN between the `books` and `categories` tables.

```sql
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
ORDER BY books.book_id;
```

The JOIN combines book information with its corresponding category.

## Pandas `read_sql()` Analysis

The project also loads SQL query results directly into Pandas using:

```python
pd.read_sql()
```

This allows SQL query results to be analysed as Pandas DataFrames.

Example columns include:

```text
title
price_gbp
price_inr
rating
```

The `read_sql()` output is included in:

```text
data_pipeline/data/query_outputs.txt
```

## SQL JOIN vs Pandas Merge

The project demonstrates two equivalent approaches for combining book and category data:

### SQL JOIN

The database performs the relationship operation directly:

```sql
JOIN categories
ON books.category_id = categories.category_id
```

### Pandas Merge

The same relationship is reproduced in memory using:

```python
pd.merge()
```

The SQL JOIN and Pandas merge results are displayed side by side.

The outputs are compared programmatically.

The completed execution verifies:

```text
Do SQL JOIN and Pandas merge produce equivalent results?
True
```

Therefore, both approaches produce equivalent results for the tested dataset.

The complete comparison is recorded in:

```text
data_pipeline/data/query_outputs.txt
```

## Output Files

The pipeline generates the following important outputs:

### Cleaned Dataset

```text
data_pipeline/data/books.csv
```

Contains the cleaned and transformed book dataset.

### Query Output Log

```text
data_pipeline/data/query_outputs.txt
```

Contains:

- SQL queries
- SQL outputs
- Pandas `read_sql()` results
- SQL JOIN results
- Pandas merge results
- JOIN vs merge comparison

### SQLite Database

The SQLite database contains:

- `books`
- `categories`

with the required primary-key and foreign-key relationship.

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite
- SQL
- Git
- GitHub

## Key Learning Outcomes

This project demonstrates practical understanding of:

### Web Scraping

Programmatically requesting web pages and extracting structured information from HTML.

### ETL

The project follows an ETL workflow:

```text
Extract
  ↓
Transform
  ↓
Load
```

- **Extract:** Scrape book information from Books to Scrape.
- **Transform:** Clean fields, convert types, and calculate INR prices.
- **Load:** Store the cleaned data in SQLite.

### Primary Key

A primary key uniquely identifies a record in a database table.

Example:

```text
book_id
category_id
```

### Foreign Key

A foreign key connects related tables.

Example:

```text
books.category_id
        ↓
categories.category_id
```

### SQL JOIN

A JOIN combines related records from multiple database tables.

### GROUP BY

`GROUP BY` creates groups that can be used with aggregation functions such as `COUNT()` and `AVG()`.

### Pandas `read_sql()`

`read_sql()` executes SQL and loads the resulting records into a Pandas DataFrame.

### Pandas `merge()`

`merge()` combines related Pandas DataFrames in memory and provides functionality similar to a SQL JOIN.

## Git Version Control

The project was developed using Git version control and a feature-branch workflow.

The repository history includes:

1. Creation of a feature branch from `main`
2. Multiple commits on the feature branch
3. Merge of the feature branch back into `main`

The feature-branch workflow is verified across the overall project repository.

## End-to-End Execution Summary

From the project root, the complete pipeline can be executed with:

```bash
python data_pipeline/src/scraper.py
python data_pipeline/src/cleaner.py
python data_pipeline/database.py
python data_pipeline/queries.py
```

The overall workflow is:

```text
Books to Scrape
       ↓
Requests + BeautifulSoup
       ↓
100 Book Records
       ↓
Data Cleaning
       ↓
Type Conversion
       ↓
GBP → INR
1 GBP = 105.50 INR
       ↓
books.csv
       ↓
SQLite
       ↓
Books + Categories Tables
       ↓
SQL Queries
       ↓
Pandas read_sql()
       ↓
SQL JOIN
       ↓
Pandas merge()
       ↓
Equivalent Results
       ↓
query_outputs.txt
```

## Project Result

The completed pipeline successfully demonstrates:

- Automated web scraping
- 100 scraped book records
- Data cleaning and transformation
- Fixed-rate GBP to INR conversion
- CSV dataset generation
- Normalized SQLite database design
- Primary and foreign key relationships
- Multiple SQL analytical queries
- SQL JOIN operations
- Pandas `read_sql()` analysis
- Pandas `merge()` analysis
- Verification that SQL JOIN and Pandas merge produce equivalent results
- Git feature-branch workflow