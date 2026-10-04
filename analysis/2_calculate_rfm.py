""" Step 2 : Feature engnieering: build Recency, Frequency, Monetary per customer 

Input : outputs/ clean_transactions.csv
Outputs: outputs/rfm_values.csv
"""

import pandas as pd

df = pd.read_csv("outputs/clean_transactions.csv", parse_dates=["InvoiceDate"])

# "Today" for the analysis = the day after the last transaction in the data.
# (Using the real today's date would make every Recency ~14 years.)

snapshot_date = df["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)
print("Snapshot date:" , snapshot_date.date())

rfm = df.groupby("CustomerID").agg(
    last_purchase=("InvoiceDate", "max"),
    Frequency=("InvoiceNo", "nunique"),   # number of DISTINCT invoices = number of orders
    Monetary=("TotalPrice", "sum"),   # total money spent
)
# Recency = days between the customer's last purchase and the snapshot date 
rfm["Recency"] = (snapshot_date - rfm["last_purchase"].dt.normalize()).dt.days
rfm = rfm[["Recency", "Frequency", "Monetary"]]

print("\nFirst 5 columns:\n", rfm.head())
print("\nSummary:\n", rfm.describe().round(1))

rfm.to_csv("outputs/rfm_values.csv")
print("\nSaved outputs/rfm_values.csv")