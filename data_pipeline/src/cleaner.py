import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

csv_file = BASE_DIR / "data" / "books.csv"

df = pd.read_csv(csv_file)

print(df.head())
print("\nData Types:")
print(df.dtypes)
# -----------------------------
# Clean Price
# -----------------------------
df["price_gbp"] = (
    df["price"]
    .str.replace("Â£", "", regex=False)
    .astype(float)
)

print("\nPrice Cleaning:")
print(df[["price", "price_gbp"]].head())

# -----------------------------
# Convert Rating
# -----------------------------
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["rating"].map(rating_map)

print("\nRating Conversion:")
print(df[["rating"]].head())

# -----------------------------
# Convert Availability
# -----------------------------
df["in_stock"] = df["availability"].str.contains("In stock")

print("\nAvailability Conversion:")
print(df[["availability", "in_stock"]].head())

# -----------------------------
# Save Cleaned Data
# -----------------------------
clean_file = BASE_DIR / "data" / "books_clean.csv"

df.to_csv(clean_file, index=False)

print("\nCleaned CSV Saved Successfully!")
print(clean_file)