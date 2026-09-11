import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =========================
# 1. Basic Settings
# =========================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


# =========================
# 2. Load Data
# =========================

df = pd.read_csv("online_retail_II_combined.csv")


# =========================
# 3. Basic Inspection
# =========================

print("=" * 60)
print("DATA SHAPE")
print("=" * 60)

print(df.shape)


print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)

print(df.head())


print("\n" + "=" * 60)
print("DATA TYPES AND NON-NULL COUNTS")
print("=" * 60)

print(df.info())


print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print(df.isnull().sum())


print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)

print(df.duplicated().sum())


print("\n" + "=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)

print(df.describe(include="all"))
# =========================
# 4. Data Quality Analysis
# =========================

print("\n" + "=" * 60)
print("NEGATIVE QUANTITY")
print("=" * 60)

negative_quantity = df[df["Quantity"] < 0]

print("Number of rows:", len(negative_quantity))
print("\nSample:")
print(
    negative_quantity[
        ["Invoice", "StockCode", "Description",
         "Quantity", "Price", "Customer ID"]
    ].head(10)
)


print("\n" + "=" * 60)
print("NEGATIVE PRICE")
print("=" * 60)

negative_price = df[df["Price"] < 0]

print("Number of rows:", len(negative_price))
print("\nSample:")
print(
    negative_price[
        ["Invoice", "StockCode", "Description",
         "Quantity", "Price", "Customer ID"]
    ].head(10)
)


print("\n" + "=" * 60)
print("ZERO PRICE")
print("=" * 60)

zero_price = df[df["Price"] == 0]

print("Number of rows:", len(zero_price))
print("\nSample:")
print(
    zero_price[
        ["Invoice", "StockCode", "Description",
         "Quantity", "Price", "Customer ID"]
    ].head(10)
)


print("\n" + "=" * 60)
print("CANCELLATION INVOICES")
print("=" * 60)

cancelled = df[df["Invoice"].str.startswith("C")]

print("Number of cancellation rows:", len(cancelled))

print("\nSample:")
print(
    cancelled[
        ["Invoice", "StockCode", "Description",
         "Quantity", "Price", "Customer ID"]
    ].head(10)
)


print("\n" + "=" * 60)
print("MISSING CUSTOMER ID")
print("=" * 60)

missing_customer = df[df["Customer ID"].isna()]

print("Number of rows:", len(missing_customer))

print("\nSample:")
print(
    missing_customer[
        ["Invoice", "StockCode", "Description",
         "Quantity", "Price", "Customer ID"]
    ].head(10)
)


print("\n" + "=" * 60)
print("MISSING DESCRIPTION")
print("=" * 60)

missing_description = df[df["Description"].isna()]

print("Number of rows:", len(missing_description))

print("\nSample:")
print(
    missing_description[
        ["Invoice", "StockCode", "Description",
         "Quantity", "Price", "Customer ID"]
    ].head(10)
)


print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)

duplicates = df[df.duplicated(keep=False)]

print("Number of duplicated rows:", len(duplicates))

print("\nSample:")
print(duplicates.head(10))
# =========================
# 5. Data Cleaning
# =========================

print("\n" + "=" * 60)
print("DATA CLEANING")
print("=" * 60)


# --------------------------------------------------
# 5.1 Convert InvoiceDate to datetime
# --------------------------------------------------

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("\nInvoiceDate dtype:")
print(df["InvoiceDate"].dtype)


# --------------------------------------------------
# 5.2 Remove exact duplicate rows
# --------------------------------------------------

before_duplicates = len(df)

df = df.drop_duplicates().copy()

after_duplicates = len(df)

print("\nDuplicate rows removed:")
print(before_duplicates - after_duplicates)

print("Rows after removing duplicates:")
print(len(df))


# --------------------------------------------------
# 5.3 Create Revenue column
# --------------------------------------------------

df["Revenue"] = df["Quantity"] * df["Price"]

print("\nRevenue column created.")

print(df[
    ["Invoice", "StockCode", "Quantity", "Price", "Revenue"]
].head())


# --------------------------------------------------
# 5.4 Create normal sales dataset
# --------------------------------------------------

sales_df = df[
    (~df["Invoice"].str.startswith("C")) &
    (df["Quantity"] > 0) &
    (df["Price"] > 0)
].copy()


print("\nNormal sales dataset:")
print("Rows:", len(sales_df))


# --------------------------------------------------
# 5.5 Customer-level dataset
# --------------------------------------------------

customer_df = sales_df[
    sales_df["Customer ID"].notna()
].copy()


print("\nCustomer analysis dataset:")
print("Rows:", len(customer_df))
print("Unique customers:",
      customer_df["Customer ID"].nunique())


# --------------------------------------------------
# 5.6 Basic validation
# --------------------------------------------------

print("\n" + "=" * 60)
print("CLEANED DATA VALIDATION")
print("=" * 60)

print("\nNegative quantity:")
print((sales_df["Quantity"] < 0).sum())

print("\nNon-positive price:")
print((sales_df["Price"] <= 0).sum())

print("\nMissing Customer ID:")
print(sales_df["Customer ID"].isna().sum())

print("\nMissing Description:")
print(sales_df["Description"].isna().sum())

print("\nTotal Revenue:")
print(round(sales_df["Revenue"].sum(), 2))

print("\nDate range:")
print(sales_df["InvoiceDate"].min())
print(sales_df["InvoiceDate"].max())
# =========================
# 6. Investigate Extreme Prices
# =========================

print("\n" + "=" * 60)
print("TOP 20 HIGHEST PRICES")
print("=" * 60)

high_price = df.sort_values(
    by="Price",
    ascending=False
)

print(
    high_price[
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "Price",
            "Customer ID",
            "Country"
        ]
    ].head(20)
)


print("\n" + "=" * 60)
print("TOP 20 HIGHEST POSITIVE PRICES IN NORMAL SALES")
print("=" * 60)

high_price_sales = sales_df.sort_values(
    by="Price",
    ascending=False
)

print(
    high_price_sales[
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "Price",
            "Customer ID",
            "Country"
        ]
    ].head(20)
)
# =========================
# 7. Investigate Non-Product Transactions
# =========================

print("\n" + "=" * 60)
print("STOCK CODES WITH HIGHEST REVENUE")
print("=" * 60)

stock_summary = (
    sales_df
    .groupby(["StockCode", "Description"], dropna=False)
    .agg(
        total_quantity=("Quantity", "sum"),
        total_revenue=("Revenue", "sum"),
        transaction_lines=("Invoice", "count")
    )
    .reset_index()
    .sort_values("total_revenue", ascending=False)
)

print(stock_summary.head(30).to_string(index=False))


print("\n" + "=" * 60)
print("NON-PRODUCT / OPERATIONAL TRANSACTIONS")
print("=" * 60)

non_product_codes = [
    "M",
    "AMAZONFEE",
    "BANK CHARGES",
    "B",
    "POST",
    "DOT",
    "ADJUST"
]

non_product_df = sales_df[
    sales_df["StockCode"].isin(non_product_codes)
].copy()

print(
    non_product_df[
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "Price",
            "Revenue",
            "Customer ID",
            "Country"
        ]
    ].head(30).to_string(index=False)
)


print("\n" + "=" * 60)
print("NON-PRODUCT REVENUE")
print("=" * 60)

print(
    non_product_df
    .groupby(["StockCode", "Description"], dropna=False)["Revenue"]
    .agg(["count", "sum"])
    .sort_values("sum", ascending=False)
)
# =========================
# 8. Create Product Sales Dataset
# =========================

print("\n" + "=" * 60)
print("CREATE PRODUCT SALES DATASET")
print("=" * 60)

# Non-product / operational transaction codes
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

print("Rows before removing non-product transactions:", len(sales_df))
print("Rows after removing non-product transactions:", len(product_sales_df))

print("\nProduct sales revenue:")
print(round(product_sales_df["Revenue"].sum(), 2))

print("\nUnique products:")
print(product_sales_df["StockCode"].nunique())

print("\nMissing Customer ID:")
print(product_sales_df["Customer ID"].isna().sum())

print("\nDate range:")
print(product_sales_df["InvoiceDate"].min())
print(product_sales_df["InvoiceDate"].max())

# =========================
# 10. Monthly Revenue Trend
# =========================

print("\n" + "=" * 60)
print("MONTHLY REVENUE TREND")
print("=" * 60)

# Aggregate revenue by month
monthly_revenue = (
    sales_df
    .groupby(sales_df["InvoiceDate"].dt.to_period("M"))["Revenue"]
    .sum()
    .reset_index()
)

# Convert Period to string for plotting
monthly_revenue["InvoiceDate"] = (
    monthly_revenue["InvoiceDate"]
    .astype(str)
)

# Rename columns
monthly_revenue.columns = ["Month", "Revenue"]

# Display results
print(monthly_revenue)


# =========================
# Plot
# =========================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue["Month"],
    monthly_revenue["Revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")

plt.xlabel("Month")
plt.ylabel("Revenue (£)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# =========================
# 11. Monthly Orders and AOV
# =========================

print("\n" + "=" * 60)
print("MONTHLY ORDERS AND AOV")
print("=" * 60)

monthly_orders_aov = (
    sales_df
    .groupby(sales_df["InvoiceDate"].dt.to_period("M"))
    .agg(
        Orders=("Invoice", "nunique"),
        Revenue=("Revenue", "sum")
    )
    .reset_index()
)

monthly_orders_aov["InvoiceDate"] = (
    monthly_orders_aov["InvoiceDate"].astype(str)
)

monthly_orders_aov.columns = ["Month", "Orders", "Revenue"]

# Calculate Average Order Value
monthly_orders_aov["AOV"] = (
    monthly_orders_aov["Revenue"]
    / monthly_orders_aov["Orders"]
)

print(monthly_orders_aov)

# =========================
# Save analysis result
# =========================

monthly_orders_aov.to_csv(
    "monthly_orders_aov.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: monthly_orders_aov.csv")


# =========================
# Plot Orders and AOV
# =========================

fig, ax1 = plt.subplots(figsize=(12, 6))

# Orders
ax1.plot(
    monthly_orders_aov["Month"],
    monthly_orders_aov["Orders"],
    marker="o",
    label="Orders"
)

ax1.set_xlabel("Month")
ax1.set_ylabel("Number of Orders")
ax1.tick_params(axis="x", rotation=45)

# AOV
ax2 = ax1.twinx()

ax2.plot(
    monthly_orders_aov["Month"],
    monthly_orders_aov["AOV"],
    marker="s",
    label="AOV"
)

ax2.set_ylabel("Average Order Value (£)")

plt.title("Monthly Orders and Average Order Value")
plt.tight_layout()

plt.savefig(
    "monthly_orders_aov.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("Saved: monthly_orders_aov.png")

# =========================
# 12. Customer Revenue Analysis
# =========================

print("\n" + "=" * 60)
print("CUSTOMER REVENUE ANALYSIS")
print("=" * 60)

customer_revenue = (
    customer_df
    .groupby("Customer ID")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique")
    )
    .reset_index()
)

customer_revenue["AOV"] = (
    customer_revenue["Revenue"]
    / customer_revenue["Orders"]
)

# Sort by revenue
customer_revenue = customer_revenue.sort_values(
    "Revenue",
    ascending=False
).reset_index(drop=True)

print("\nTop 20 Customers by Revenue:")
print(customer_revenue.head(20))


# =========================
# Save customer analysis
# =========================

customer_revenue.to_csv(
    "customer_revenue_analysis.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: customer_revenue_analysis.csv")


# =========================
# Top 10 Customers
# =========================

top10 = customer_revenue.head(10)

print("\n" + "=" * 60)
print("TOP 10 CUSTOMERS")
print("=" * 60)

print(top10)


# =========================
# Top 10 Revenue Share
# =========================

total_customer_revenue = customer_revenue["Revenue"].sum()

top10_revenue = top10["Revenue"].sum()

top10_share = (
    top10_revenue
    / total_customer_revenue
    * 100
)

print(
    f"\nTop 10 customers revenue share: "
    f"{top10_share:.2f}%"
)


# =========================
# Plot Top 10 Customers
# =========================

plt.figure(figsize=(10, 6))

plt.bar(
    top10["Customer ID"].astype(str),
    top10["Revenue"]
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Customer ID")
plt.ylabel("Revenue (£)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "top10_customers_revenue.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("Saved: top10_customers_revenue.png")