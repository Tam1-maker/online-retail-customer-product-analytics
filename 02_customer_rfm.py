import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


# =========================
# 1. Load Data
# =========================

df = pd.read_csv("online_retail_II_combined.csv")

print("=" * 60)
print("DATA LOADING")
print("=" * 60)

print("Original shape:", df.shape)


# =========================
# 2. Data Cleaning
# =========================

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Remove exact duplicate rows
df = df.drop_duplicates().copy()

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["Price"]


# Keep normal sales transactions
sales_df = df[
    (~df["Invoice"].str.startswith("C")) &
    (df["Quantity"] > 0) &
    (df["Price"] > 0)
].copy()


# Keep transactions with Customer ID
customer_df = sales_df[
    sales_df["Customer ID"].notna()
].copy()


print("\nAfter cleaning:")
print("Sales rows:", len(sales_df))
print("Customer transaction rows:", len(customer_df))
print(
    "Unique customers:",
    customer_df["Customer ID"].nunique()
)


# =========================
# 3. Customer-level Metrics
# =========================

customer_rfm = (
    customer_df
    .groupby("Customer ID")
    .agg(
        Recency=("InvoiceDate", "max"),
        Frequency=("Invoice", "nunique"),
        Monetary=("Revenue", "sum")
    )
    .reset_index()
)


# =========================
# 4. Calculate Recency
# =========================

analysis_date = customer_df["InvoiceDate"].max()

customer_rfm["Recency"] = (
    analysis_date - customer_rfm["Recency"]
).dt.days


print("\n" + "=" * 60)
print("RFM DATA")
print("=" * 60)

print(customer_rfm.head(10))


# =========================
# 5. RFM Descriptive Statistics
# =========================

print("\n" + "=" * 60)
print("RFM DESCRIPTIVE STATISTICS")
print("=" * 60)

print(
    customer_rfm[
        ["Recency", "Frequency", "Monetary"]
    ].describe()
)


# =========================
# 6. Save RFM Dataset
# =========================

customer_rfm.to_csv(
    "customer_rfm.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: customer_rfm.csv")
# =========================
# 7. RFM Scoring
# =========================

print("\n" + "=" * 60)
print("RFM SCORING")
print("=" * 60)

# Recency:
# Smaller Recency = better customer
customer_rfm["R_Score"] = pd.qcut(
    customer_rfm["Recency"],
    5,
    labels=[5, 4, 3, 2, 1]
)

# Frequency:
# Higher Frequency = better customer
customer_rfm["F_Score"] = pd.qcut(
    customer_rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
)

# Monetary:
# Higher Monetary = better customer
customer_rfm["M_Score"] = pd.qcut(
    customer_rfm["Monetary"],
    5,
    labels=[1, 2, 3, 4, 5]
)

# Convert scores to integers
customer_rfm["R_Score"] = customer_rfm["R_Score"].astype(int)
customer_rfm["F_Score"] = customer_rfm["F_Score"].astype(int)
customer_rfm["M_Score"] = customer_rfm["M_Score"].astype(int)


# =========================
# 8. RFM Score
# =========================

customer_rfm["RFM_Score"] = (
    customer_rfm["R_Score"].astype(str)
    + customer_rfm["F_Score"].astype(str)
    + customer_rfm["M_Score"].astype(str)
)

print(customer_rfm.head(20))


# =========================
# 9. Customer Segmentation
# =========================

def segment_customer(row):

    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4 and m >= 3:
        return "Loyal Customers"

    elif r >= 4 and m >= 4 and f < 4:
        return "Big Spenders"

    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"

    elif r <= 2 and f <= 2:
        return "Lost Customers"

    else:
        return "Others"


customer_rfm["Segment"] = customer_rfm.apply(
    segment_customer,
    axis=1
)


# =========================
# 10. Segment Summary
# =========================

segment_summary = (
    customer_rfm
    .groupby("Segment")
    .agg(
        Customers=("Customer ID", "count"),
        Revenue=("Monetary", "sum"),
        Avg_Revenue=("Monetary", "mean"),
        Avg_Orders=("Frequency", "mean")
    )
    .reset_index()
)

segment_summary["Revenue_Share"] = (
    segment_summary["Revenue"]
    / segment_summary["Revenue"].sum()
    * 100
)

segment_summary = segment_summary.sort_values(
    "Revenue",
    ascending=False
)

print("\n" + "=" * 60)
print("CUSTOMER SEGMENT SUMMARY")
print("=" * 60)

print(segment_summary)


# =========================
# 11. Save RFM Results
# =========================

customer_rfm.to_csv(
    "customer_rfm.csv",
    index=False,
    encoding="utf-8-sig"
)

segment_summary.to_csv(
    "customer_segment_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: customer_rfm.csv")
print("Saved: customer_segment_summary.csv")
# =========================
# 12. Customer Segment Visualization
# =========================

print("\n" + "=" * 60)
print("CUSTOMER SEGMENT VISUALIZATION")
print("=" * 60)


# Sort segments by number of customers
segment_customer_count = (
    segment_summary
    .sort_values("Customers", ascending=False)
)


# =========================
# Customer Count by Segment
# =========================

plt.figure(figsize=(10, 6))

plt.bar(
    segment_customer_count["Segment"],
    segment_customer_count["Customers"]
)

plt.title("Customer Distribution by RFM Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "customer_segment_distribution.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("Saved: customer_segment_distribution.png")


# =========================
# Revenue Share by Segment
# =========================

segment_revenue_share = (
    segment_summary
    .sort_values("Revenue_Share", ascending=False)
)


plt.figure(figsize=(10, 6))

plt.bar(
    segment_revenue_share["Segment"],
    segment_revenue_share["Revenue_Share"]
)

plt.title("Revenue Share by RFM Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue Share (%)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "customer_segment_revenue_share.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("Saved: customer_segment_revenue_share.png")