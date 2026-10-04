"""STEP 5 (Bonus) - Visualise RFM segments with Seaborn heatmaps and bar charts.

Input : outputs/rfm_segments.csv, outputs/segment_summary.csv
Output: outputs/*.png
"""
import matplotlib
matplotlib.use("Agg")                # save to files, no pop-up window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
rfm = pd.read_csv("outputs/rfm_segments.csv", index_col="CustomerID")
summary = pd.read_csv("outputs/segment_summary.csv", index_col="Segment")
order = summary.index.tolist()       # biggest revenue first


def save(name):
    plt.tight_layout(); plt.savefig(f"outputs/{name}", dpi=150); plt.close()
    print("saved", name)


# 1) Distribution of R, F, M (log scale for F and M because a few customers spend huge amounts)
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(rfm["Recency"], bins=40, ax=ax[0], color="#4c72b0").set_title("Recency (days)")
sns.histplot(np.log1p(rfm["Frequency"]), bins=40, ax=ax[1], color="#55a868").set_title("Frequency (log scale)")
sns.histplot(np.log1p(rfm["Monetary"]), bins=40, ax=ax[2], color="#c44e52").set_title("Monetary (log scale)")
save("1_rfm_distributions.png")

# 2) Bar chart: how many customers per segment
plt.figure(figsize=(8, 5))
sns.barplot(x="Customers", y=summary.index, data=summary, order=order, hue=summary.index, legend=False, palette="viridis")
plt.title("Number of customers per segment"); plt.ylabel("")
save("2_customers_per_segment.png")

# 3) Bar chart: share of revenue per segment
plt.figure(figsize=(8, 5))
sns.barplot(x="Pct_Revenue", y=summary.index, data=summary, order=order, hue=summary.index, legend=False, palette="viridis")
plt.title("% of total revenue per segment"); plt.ylabel("")
save("3_revenue_per_segment.png")

# 4) Heatmap: average spend for each Recency x Frequency score
pivot = rfm.pivot_table(index="R", columns="F", values="Monetary", aggfunc="mean").sort_index(ascending=False)
plt.figure(figsize=(7, 5.5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={"label": "Average spend"})
plt.title("Average spend by Recency (R) and Frequency (F) score")
save("4_heatmap_rf_spend.png")

# 5) Heatmap: how many customers in each Recency x Frequency cell
counts = rfm.pivot_table(index="R", columns="F", values="Monetary", aggfunc="count").sort_index(ascending=False)
plt.figure(figsize=(7, 5.5))
sns.heatmap(counts, annot=True, fmt=".0f", cmap="Oranges", cbar_kws={"label": "Customers"})
plt.title("Customers by Recency (R) and Frequency (F) score")
save("5_heatmap_rf_count.png")

# 6) Heatmap: profile of each segment (colour = relative level, numbers = real averages)
prof = summary[["Avg_Recency", "Avg_Frequency", "Avg_Monetary"]]
norm = (prof - prof.min()) / (prof.max() - prof.min())
plt.figure(figsize=(7.5, 5.5))
sns.heatmap(norm, annot=prof, fmt=".0f", cmap="RdYlGn_r", cbar=False)
plt.title("Segment profiles (numbers = average values)")
save("6_segment_profile_heatmap.png")