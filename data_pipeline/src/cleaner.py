import pandas as pd
from pathlib import Path


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

csv_file = BASE_DIR / "data" / "books.csv"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(csv_file)

print("CSV loaded successfully!")
print(f"Rows loaded: {len(df)}")


# --------------------------------------------------
# CLEAN PRICE
# --------------------------------------------------

df["price_gbp"] = pd.to_numeric(
    df["price_gbp"],
    errors="coerce"
)


# --------------------------------------------------
# CONVERT RATING
# --------------------------------------------------

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)


# --------------------------------------------------
# CONVERT AVAILABILITY / STOCK
# --------------------------------------------------

df["in_stock"] = df["in_stock"].astype(bool)


# --------------------------------------------------
# GBP → INR
# --------------------------------------------------

GBP_TO_INR = 105.50

df["price_inr"] = (
    df["price_gbp"] * GBP_TO_INR
).round(2)


# --------------------------------------------------
# HANDLE INVALID NUMERIC VALUES
# --------------------------------------------------

if df["price_gbp"].isna().any():

    median_price = df["price_gbp"].median()

    df["price_gbp"] = df["price_gbp"].fillna(
        median_price
    )

    print(
        f"Missing price values replaced with median: "
        f"{median_price}"
    )


if df["rating"].isna().any():

    median_rating = round(
        df["rating"].median()
    )

    df["rating"] = df["rating"].fillna(
        median_rating
    )

    print(
        f"Missing rating values replaced with median: "
        f"{median_rating}"
    )


# --------------------------------------------------
# FINAL COLUMN ORDER
# --------------------------------------------------

df = df[
    [
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category"
    ]
]


# --------------------------------------------------
# DISPLAY FINAL DATA
# --------------------------------------------------

print("\nFinal Data:")
print(df.head())

print("\nData Types:")
print(df.dtypes)


# --------------------------------------------------
# SAVE CLEANED DATA
# --------------------------------------------------

df.to_csv(csv_file, index=False)

print("\nCleaned CSV saved successfully!")
print(f"Location: {csv_file}")