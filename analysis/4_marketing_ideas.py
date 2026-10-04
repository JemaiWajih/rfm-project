"""STEP 4 - Simple marketing idea for each segment.

Input : outputs/segment_summary.csv
Output: outputs/marketing_ideas.csv
"""
import pandas as pd

IDEAS = {
    "Champions":           "Reward them: VIP perks, early access to new products, referral bonus. No big discounts needed.",
    "Loyal Customers":     "Loyalty points, product bundles, upsell higher-value items.",
    "Potential Loyalists": "Invite to loyalty programme, 'buy again' emails, cross-sell related products.",
    "New Customers":       "Welcome email series and a small discount on the 2nd order.",
    "Need Attention":      "Limited-time offers and personalised reminders before they drift away.",
    "About to Sleep":      "Cheap reactivation: reminder email, popular-items digest, free-shipping nudge.",
    "Can't Lose Them":     "Top-priority win-back: personal outreach, strong 'we miss you' discount, ask why they left.",
    "At Risk":             "Win-back campaign with a discount on categories they used to buy.",
    "Hibernating":         "Occasional low-cost clearance offers. Don't over-invest.",
    "Lost":                "One last re-engagement email, then stop spending marketing money on them.",
}

summary = pd.read_csv("outputs/segment_summary.csv", index_col="Segment")
summary["Marketing_Idea"] = summary.index.map(IDEAS)

table = summary[["Customers", "Pct_Customers", "Pct_Revenue", "Marketing_Idea"]]
for seg, row in table.iterrows():
    print(f"\n{seg}  ({row['Customers']:.0f} customers, {row['Pct_Revenue']}% of revenue)\n  -> {row['Marketing_Idea']}")

table.to_csv("outputs/marketing_ideas.csv")
print("\nSaved outputs/marketing_ideas.csv")