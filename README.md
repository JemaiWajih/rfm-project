# Customer Segmentation Using RFM Analysis

**Level 2 – Task 3** · Segment the customers of an online retailer by **Recency, Frequency and Monetary** value, group similar customers, and suggest a marketing action for each group.

- **Tools:** Python, Pandas, Seaborn (Matplotlib is used by Seaborn to save the charts)
- **Dataset:** [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online-retail) – about 541,909 transactions from a UK-based online gift retailer (Dec 2010 – Dec 2011)

---

## Project structure

```
rfm-project/
├── analysis/
│   ├── 1_load_and_clean.py        # load the dataset and clean it
│   ├── 2_calculate_rfm.py         # Recency, Frequency, Monetary per customer
│   ├── 3_score_and_segment.py     # scores 1-5, then group similar customers
│   ├── 4_marketing_ideas.py       # a marketing idea for each segment
│   └── 5_visualize.py             # bonus: Seaborn heatmaps and bar charts
├── data/
│   └── Online Retail.xlsx         # raw dataset (download it, see below)
├── outputs/
│   ├── clean_transactions.csv     # step 1 result
│   ├── rfm_values.csv             # step 2 result
│   ├── rfm_segments.csv           # step 3 result: one row per customer
│   ├── segment_summary.csv        # step 3 result: one row per segment
│   ├── marketing_ideas.csv        # step 4 result
│   ├── 1_rfm_distributions.png    # step 5 charts
│   ├── 2_customers_per_segment.png
│   ├── 3_revenue_per_segment.png
│   ├── 4_heatmap_rf_spend.png
│   ├── 5_heatmap_rf_count.png
│   └── 6_segment_profile_heatmap.png
├── venv/                          # virtual environment (not part of the project code)
├── .gitignore
├── requirements.txt
└── run_all.py                     # runs steps 1-5 in order
```

## How the files match the task

| Task requirement | File |
|---|---|
| Use the Online Retail dataset | `analysis/1_load_and_clean.py` |
| Recency, Frequency, Monetary | `analysis/2_calculate_rfm.py` |
| Assign scores to each customer | `analysis/3_score_and_segment.py` |
| Group similar customers | `analysis/3_score_and_segment.py` |
| Suggest marketing ideas per group | `analysis/4_marketing_ideas.py` |
| Bonus: heatmaps or bar charts | `analysis/5_visualize.py` |

## Setup and run

**1. Get the data.** Download `Online Retail.xlsx` from the [UCI page](https://archive.ics.uci.edu/dataset/352/online-retail) and place it in `data/`.

**2. Create a virtual environment and install the libraries** (Linux / macOS):
```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt   # pandas, seaborn, matplotlib, openpyxl
```

**3. Run everything** from the project root (the folder that contains `analysis/`, `data/` and `outputs/`):
```bash
python run_all.py
```

To run a single step, also run it from the project root, because the scripts use relative paths such as `data/` and `outputs/`. Earlier steps must have been run first:
```bash
python analysis/3_score_and_segment.py
```

Reading the `.xlsx` can take about a minute.

## What each step does

| Step | Input | What happens | Output |
|---|---|---|---|
| 1. Load and clean | `data/Online Retail.xlsx` | Removes rows with no `CustomerID`, cancelled invoices (starting with "C"), quantity or price ≤ 0, and duplicates. Adds `TotalPrice = Quantity × UnitPrice`. | `clean_transactions.csv` |
| 2. Calculate RFM | `clean_transactions.csv` | Builds one row per customer: **Recency** (days since last purchase, measured from the day after the last transaction), **Frequency** (number of distinct invoices), **Monetary** (total spend). | `rfm_values.csv` |
| 3. Score and segment | `rfm_values.csv` | Scores each metric from 1 to 5 using quintiles (Recency reversed, so recent = 5), then assigns each customer to one of 10 segments. | `rfm_segments.csv`, `segment_summary.csv` |
| 4. Marketing ideas | `segment_summary.csv` | Adds a suggested action for each segment. | `marketing_ideas.csv` |
| 5. Visualize | `rfm_segments.csv`, `segment_summary.csv` | Draws distributions, bar charts and heatmaps. | `outputs/*.png` |

## RFM in one minute

- **Recency** – days since the last purchase (lower is better)
- **Frequency** – number of orders (higher is better)
- **Monetary** – total money spent (higher is better)

Each metric is scored 1–5 (the top 20% of customers get a 5; Recency is reversed). Customers are then grouped using Recency against the average of their Frequency and Monetary scores, for example **Champions**, **Loyal Customers**, **At Risk** and **Lost**.

## Results

From `outputs/segment_summary.csv`: **4,338 customers** and about **£8.89 million** in revenue.

| Segment | Customers | % of customers | % of revenue | Avg recency (days) | Avg orders | Avg spend (£) | Marketing idea |
|---|---:|---:|---:|---:|---:|---:|---|
| Champions | 747 | 17.2 | 61.5 | 12.5 | 13.0 | 7,320 | Reward them: VIP perks, early access, referral bonus |
| Loyal Customers | 799 | 18.4 | 18.0 | 31.4 | 4.6 | 2,003 | Loyalty points, bundles, upsell |
| At Risk | 587 | 13.5 | 6.3 | 166.3 | 2.3 | 957 | Win-back campaign with a targeted discount |
| Can't Lose Them | 204 | 4.7 | 6.1 | 126.0 | 5.3 | 2,669 | Personal outreach and a strong "we miss you" offer |
| Need Attention | 304 | 7.0 | 2.1 | 52.7 | 1.8 | 609 | Limited-time offers and reminders |
| Potential Loyalists | 275 | 6.3 | 1.9 | 16.5 | 2.3 | 607 | Loyalty programme invite, cross-sell |
| Lost | 609 | 14.0 | 1.7 | 278.4 | 1.1 | 244 | One last re-engagement email, then stop spending |
| Hibernating | 335 | 7.7 | 1.1 | 120.4 | 1.1 | 285 | Occasional low-cost clearance offers |
| New Customers | 283 | 6.5 | 0.8 | 18.4 | 1.2 | 257 | Welcome series and a small discount on the 2nd order |
| About to Sleep | 195 | 4.5 | 0.5 | 53.1 | 1.0 | 223 | Cheap reactivation reminders |

### Key findings

1. **Revenue is highly concentrated.** Champions are 17.2% of customers but bring in 61.5% of revenue. Champions and Loyal Customers together are about 36% of customers and about 80% of revenue. Protecting these two groups is the top priority.
2. **There is a clear win-back opportunity.** *At Risk* and *Can't Lose Them* make up about 18% of customers and about £1.1 million (12.4%) of revenue. They used to buy well but have been inactive for 4–5+ months, and *Can't Lose Them* has the higher spend per customer, so it should be contacted first.
3. **Low-value groups need low-cost actions.** *Lost*, *Hibernating* and *About to Sleep* are about 26% of customers but only about 3% of revenue, so avoid spending heavily on them.
4. **New Customers and Potential Loyalists are the growth pool.** They are recent buyers (about 17–18 days since last order) with low spend, so the goal is to get a second and third purchase.

## Limitations

- The data covers only about one year, so seasonality (e.g. the Christmas gift peak) can affect Recency.
- Many customers are wholesalers, which inflates Frequency and Monetary for the top segments.
- Around a quarter of the rows have no `CustomerID` and were excluded, so the results describe identified customers only.
- Monetary is revenue, not profit, and the segment rules are a convention that can be tuned to the business.
