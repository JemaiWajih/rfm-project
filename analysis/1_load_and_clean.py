""" STEP 1 - Load the Online retail dataset and clean it  """

from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

def find_data_file():
    for name in ["Online Retail.xlsx", "Online_Retail.csv", "OnlineRetail.csv"]:
        if (DATA_DIR/name).exists():
            return DATA_DIR / name
        raise FileNotFoundError("Put 'Online_Retail_xlsx' inside the data/ folder ")

    
path = find_data_file()
print("Loading:", path)
if path.suffix == ".xlsx":
    df = pd.read_excel(path)
else:
    try:
        df = pd.read_csv(path)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="ISO-8859-1")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
print("Raw rows:", len(df))
print("nMissing values per column:\n", df.isna().sum())

# Cleaning
n = len(df)

# 1) RFM is per customer, so rows without a CustomerID are useless.
df = df.dropna(subset=["CustomerID"])
print(f"\nRemoved {n - len(df):>7,} rows with no CustomerID"); n = len(df)

# 2) InvoiceNo starting with "C" = cancelled order, not a real purchase.
df["InvoiceNo"] = df["InvoiceNo"].astype(str)
df = df[~df["InvoiceNo"].str.startswith("C")]
print(f"Removed {n -len(df):>7,} cancelled invoice"); n = len(df)


# 3) Negative/zero quantity or price = returns, free items, data erros.
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0 )]
print(f"Removed {n - len(df):>7,} rows with quantity or price <= 0"); n = len(df)


# 4) Exact duplicate rows would double count spending.
df = df.drop_duplicates()
print(f"Removed {n - len(df):>7,} duplicate rows")

# New column: how much money each row is worth
df["CustomerID"] = df["CustomerID"].astype(int)
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

print(f"n\Clean rows: {len(df):,} | Customers: {df['CustomerID'].nunique():,}")
print("Period:", df["InvoiceDate"].min().date(), "->",
df["InvoiceDate"].max().date())

df.to_csv(OUT_DIR / "clean_transactions.csv", index=False)
print("Saved outputs/clean_transcations.csv")