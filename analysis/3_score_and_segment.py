"""Step3 - Assign R/F/M scores (1-5) and group customers into segments.

Input: outputs/rfm_values.csv
Outputs: outputs/rfm_segments.csv, outputs/segments_summary.csv
"""

import pandas as pd

rfm = pd.read_csv("outputs/rfm_values.csv", index_col="CustomerID")

# Scoring: split customers into 5 equal groups (quintiles) per metric
# rank(method= "first") breaks ties so the 5 groups always exist
# (many customers have frequency = 1, which would otherwise break qcut).

rfm["R"] = pd.qcut(rfm["Recency"].rank(method="first"), 5, labels=[5,4,3,2,1]).astype(int)
rfm["F"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["RFM_Score"] = rfm["R"].astype(str) + rfm["F"].astype(str) + rfm["M"].astype(str)  # e.g. "555"


# ---- Segmentation logic: compare Recency with the average of Frequency and Monetary ----
def segment(row):
    r = row["R"]
    fm = (row["F"] + row["M"]) / 2      # "how valuable" (spend + loyalty)
    if r >= 4 and fm >= 4.5: return "Champions"
    if r >= 3 and fm >= 3.5: return "Loyal Customers"
    if r >= 4 and fm >= 2.5: return "Potential Loyalists"
    if r >= 4:               return "New Customers"
    if r == 3 and fm >= 2:   return "Need Attention"
    if r == 3:               return "About to Sleep"
    if r <= 2 and fm >= 4:   return "Can't Lose Them"
    if r <= 2 and fm >= 2.5: return "At Risk"
    if r == 2:               return "Hibernating"
    return "Lost"


rfm["Segment"] = rfm.apply(segment, axis=1)

# ---- Profile each segment ----
summary = rfm.groupby("Segment").agg(
    Customers=("Recency", "size"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum"),
)
summary["Pct_Customers"] = summary["Customers"] / summary["Customers"].sum() * 100
summary["Pct_Revenue"] = summary["Total_Revenue"] / summary["Total_Revenue"].sum() * 100
summary = summary.round(1).sort_values("Total_Revenue", ascending=False)

pd.set_option("display.width", 200)
print(summary)

rfm.to_csv("outputs/rfm_segments.csv")
summary.to_csv("outputs/segment_summary.csv")
print("\nSaved outputs/rfm_segments.csv and outputs/segment_summary.csv")