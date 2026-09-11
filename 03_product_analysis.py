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


print("\nAfter cleaning:")
print("Sales rows:", len(sales_df))
print(
    "Sales revenue:",
    f"£{sales_df['Revenue'].sum():,.2f}"
)


# =========================
# 3. Remove Non-Product Transactions
# =========================

non_product_codes = [
    "M",
    "AMAZONFEE",
    "BANK CHARGES",
    "B",
    "POST",
    "DOT",
    "ADJUST"
]

product_sales_df = sales_df[
    ~sales_df["StockCode"].isin(non_product_codes)
].copy()


print("\n" + "=" * 60)
print("PRODUCT SALES DATA")
print("=" * 60)

print(
    "Rows before removing non-product transactions:",
    len(sales_df)
)

print(
    "Rows after removing non-product transactions:",
    len(product_sales_df)
)

print(
    "Product revenue:",
    f"£{product_sales_df['Revenue'].sum():,.2f}"
)

print(
    "Unique products:",
    product_sales_df["StockCode"].nunique()
)


# =========================
# 4. Product-level Analysis
# =========================

product_summary = (
    product_sales_df
    .groupby("StockCode")
    .agg(
        Description=("Description", "first"),
        Quantity=("Quantity", "sum"),
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique")
    )
    .reset_index()
)


# Calculate average selling price
product_summary["Avg_Price"] = (
    product_summary["Revenue"]
    / product_summary["Quantity"]
)


# Sort by revenue
product_summary = product_summary.sort_values(
    "Revenue",
    ascending=False
).reset_index(drop=True)


# =========================
# 5. Revenue Share
# =========================

total_product_revenue = product_summary["Revenue"].sum()

product_summary["Revenue_Share"] = (
    product_summary["Revenue"]
    / total_product_revenue
    * 100
)


print("\n" + "=" * 60)
print("TOP 20 PRODUCTS BY REVENUE")
print("=" * 60)

print(
    product_summary.head(20).to_string(
        index=False,
        formatters={
            "Revenue": "£{:,.2f}".format,
            "Avg_Price": "£{:,.2f}".format,
            "Revenue_Share": "{:.2f}%".format
        }
    )
)


# =========================
# 6. Save Product Dataset
# =========================

product_summary.to_csv(
    "product_analysis.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: product_analysis.csv")


# =========================
# 7. Top 10 Products by Revenue
# =========================

top10_products = product_summary.head(10)


plt.figure(figsize=(12, 6))

plt.bar(
    top10_products["StockCode"].astype(str),
    top10_products["Revenue"]
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Stock Code")
plt.ylabel("Revenue (£)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "top10_products_revenue.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("Saved: top10_products_revenue.png")


# =========================
# 8. Top 10 Products by Quantity
# =========================

top10_quantity = (
    product_summary
    .sort_values("Quantity", ascending=False)
    .head(10)
)


print("\n" + "=" * 60)
print("TOP 10 PRODUCTS BY QUANTITY")
print("=" * 60)

print(
    top10_quantity[
        ["StockCode", "Description", "Quantity", "Revenue"]
    ].to_string(index=False)
)


plt.figure(figsize=(12, 6))

plt.bar(
    top10_quantity["StockCode"].astype(str),
    top10_quantity["Quantity"]
)

plt.title("Top 10 Products by Sales Volume")
plt.xlabel("Stock Code")
plt.ylabel("Quantity Sold")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "top10_products_quantity.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("Saved: top10_products_quantity.png")


# =========================
# 9. Revenue vs Quantity
# =========================

plt.figure(figsize=(10, 6))

plt.scatter(
    product_summary["Quantity"],
    product_summary["Revenue"],
    alpha=0.5
)

plt.title("Product Sales Volume vs Revenue")
plt.xlabel("Quantity Sold")
plt.ylabel("Revenue (£)")

plt.tight_layout()

plt.savefig(
    "product_quantity_vs_revenue.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("Saved: product_quantity_vs_revenue.png")


# =========================
# 10. Key Findings
# =========================

top_revenue_product = product_summary.iloc[0]

top_quantity_product = (
    product_summary
    .sort_values("Quantity", ascending=False)
    .iloc[0]
)

print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)

print(
    "Top product by revenue:",
    top_revenue_product["StockCode"],
    "-",
    top_revenue_product["Description"]
)

print(
    f"Revenue: £{top_revenue_product['Revenue']:,.2f}"
)

print(
    "\nTop product by quantity:",
    top_quantity_product["StockCode"],
    "-",
    top_quantity_product["Description"]
)

print(
    f"Quantity: {top_quantity_product['Quantity']:,}"
)

print(
    f"\nTop product revenue share: "
    f"{top_revenue_product['Revenue_Share']:.2f}%"
)
# =========================
# 11. Product Data Quality Check
# =========================

print("\n" + "=" * 60)
print("PRODUCT DATA QUALITY CHECK")
print("=" * 60)

# Products with very high quantity but very few orders
suspicious_products = product_summary[
    (product_summary["Quantity"] >= 50000) &
    (product_summary["Orders"] <= 5)
].copy()

print("\nPotentially unusual products:")
print(
    suspicious_products[
        [
            "StockCode",
            "Description",
            "Quantity",
            "Revenue",
            "Orders",
            "Avg_Price"
        ]
    ].to_string(index=False)
)


# Save for further investigation
suspicious_products.to_csv(
    "suspicious_products.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: suspicious_products.csv")
# =========================
# 13. Product Value Matrix
# =========================

print("\n" + "=" * 60)
print("PRODUCT VALUE MATRIX")
print("=" * 60)

revenue_median = product_summary["Revenue"].median()
quantity_median = product_summary["Quantity"].median()

product_matrix = product_summary.copy()

product_matrix["Revenue_Level"] = np.where(
    product_matrix["Revenue"] >= revenue_median,
    "High Revenue",
    "Low Revenue"
)

product_matrix["Volume_Level"] = np.where(
    product_matrix["Quantity"] >= quantity_median,
    "High Volume",
    "Low Volume"
)

product_matrix["Product_Segment"] = np.select(
    [
        (product_matrix["Revenue_Level"] == "High Revenue") &
        (product_matrix["Volume_Level"] == "High Volume"),

        (product_matrix["Revenue_Level"] == "High Revenue") &
        (product_matrix["Volume_Level"] == "Low Volume"),

        (product_matrix["Revenue_Level"] == "Low Revenue") &
        (product_matrix["Volume_Level"] == "High Volume")
    ],
    [
        "High Value / High Volume",
        "High Value / Low Volume",
        "Low Value / High Volume"
    ],
    default="Low Value / Low Volume"
)

print("\nRevenue median:")
print(f"£{revenue_median:,.2f}")

print("\nQuantity median:")
print(f"{quantity_median:,.0f}")

print("\nProduct segment distribution:")
print(
    product_matrix["Product_Segment"]
    .value_counts()
)

print("\nTop products in each segment:")

for segment in [
    "High Value / High Volume",
    "High Value / Low Volume",
    "Low Value / High Volume",
    "Low Value / Low Volume"
]:

    print("\n" + "-" * 40)
    print(segment)

    segment_df = product_matrix[
        product_matrix["Product_Segment"] == segment
    ].head(5)

    print(
        segment_df[
            [
                "StockCode",
                "Description",
                "Quantity",
                "Revenue",
                "Orders"
            ]
        ].to_string(index=False)
    )


# Save product matrix
product_matrix.to_csv(
    "product_value_matrix.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: product_value_matrix.csv")


# =========================
# 14. Product Value Matrix Plot
# =========================

plt.figure(figsize=(10, 7))

plt.scatter(
    product_matrix["Quantity"],
    product_matrix["Revenue"],
    alpha=0.5
)

# Median reference lines
plt.axvline(
    quantity_median,
    linestyle="--"
)

plt.axhline(
    revenue_median,
    linestyle="--"
)

# Log scale to handle highly skewed product distribution
plt.xscale("log")
plt.yscale("log")

plt.title("Product Value Matrix (Log Scale)")
plt.xlabel("Quantity Sold (log scale)")
plt.ylabel("Revenue (£, log scale)")

plt.tight_layout()

plt.savefig(
    "product_value_matrix.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("Saved: product_value_matrix.png")