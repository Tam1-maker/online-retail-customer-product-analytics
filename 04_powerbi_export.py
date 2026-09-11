import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


# ============================================================
# 1. DATA LOADING
# ============================================================

print("=" * 60)
print("POWER BI DATA EXPORT")
print("=" * 60)

df = pd.read_csv("online_retail_II_combined.csv")

print("Original shape:", df.shape)


# ============================================================
# 2. DATA CLEANING
# ============================================================

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Remove exact duplicate rows
df = df.drop_duplicates().copy()

# Revenue
df["Revenue"] = df["Quantity"] * df["Price"]

# Normal sales transactions
sales_df = df[
    (~df["Invoice"].str.startswith("C")) &
    (df["Quantity"] > 0) &
    (df["Price"] > 0)
].copy()

print("\nAfter cleaning:")
print("Sales rows:", len(sales_df))
print(f"Sales revenue: £{sales_df['Revenue'].sum():,.2f}")


# ============================================================
# 3. SALES CLEAN DATASET
# ============================================================

sales_export = sales_df[
    [
        "Invoice",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "Price",
        "Customer ID",
        "Country",
        "Revenue"
    ]
].copy()

sales_export.to_csv(
    "sales_clean.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved: sales_clean.csv")


# ============================================================
# 4. MONTHLY SALES
# ============================================================

monthly_sales = (
    sales_df
    .groupby(
        sales_df["InvoiceDate"].dt.to_period("M")
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

monthly_sales["InvoiceDate"] = (
    monthly_sales["InvoiceDate"]
    .astype(str)
)

monthly_sales["AOV"] = (
    monthly_sales["Revenue"]
    / monthly_sales["Orders"]
)

monthly_sales.columns = [
    "Month",
    "Revenue",
    "Orders",
    "Quantity",
    "AOV"
]

monthly_sales.to_csv(
    "monthly_sales.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Saved: monthly_sales.csv")


# ============================================================
# 5. TOP CUSTOMERS
# ============================================================

customer_sales = sales_df[
    sales_df["Customer ID"].notna()
].copy()

top_customers = (
    customer_sales
    .groupby("Customer ID")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

top_customers["AOV"] = (
    top_customers["Revenue"]
    / top_customers["Orders"]
)

top_customers = top_customers.sort_values(
    "Revenue",
    ascending=False
)

top_customers.to_csv(
    "customer_sales_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Saved: customer_sales_summary.csv")


# ============================================================
# 6. DATA VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("POWER BI DATA VALIDATION")
print("=" * 60)

print("\nSales rows:")
print(len(sales_export))

print("\nSales revenue:")
print(f"£{sales_export['Revenue'].sum():,.2f}")

print("\nUnique invoices:")
print(sales_export["Invoice"].nunique())

print("\nUnique customers:")
print(sales_export["Customer ID"].nunique())

print("\nUnique products:")
print(sales_export["StockCode"].nunique())

print("\nDate range:")
print(
    sales_export["InvoiceDate"].min(),
    "to",
    sales_export["InvoiceDate"].max()
)

print("\nMissing Customer ID:")
print(sales_export["Customer ID"].isna().sum())

print("\nNegative quantity:")
print((sales_export["Quantity"] < 0).sum())

print("\nNon-positive price:")
print((sales_export["Price"] <= 0).sum())


print("\n" + "=" * 60)
print("EXPORT COMPLETE")
print("=" * 60)