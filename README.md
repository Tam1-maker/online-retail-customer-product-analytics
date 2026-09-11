# Online Retail Customer & Product Analytics

## Project Overview

This project analyzes two years of transaction data from an online retailer to understand sales performance, customer value, and product performance.

The main business question is:

> How can the retailer improve customer retention and maximize customer value through data-driven customer and product analysis?

The project combines Python, SQL, PostgreSQL, RFM analysis, and Streamlit to transform raw transaction data into actionable business insights.

---

## Business Objectives

The analysis focuses on four key questions:

1. How does sales performance change over time?
2. Which customers generate the highest value?
3. Which customer segments should the business prioritize?
4. Which products drive revenue and sales volume?

---

## Dataset

The project uses the **Online Retail II** dataset from the UCI Machine Learning Repository.

The dataset contains more than 1 million transaction records covering approximately two years of sales activity.

### Dataset characteristics

- Records: 1,067,371
- Period: December 2009 – December 2011
- Countries: 43
- Variables: 8
- Business type: UK-based online retailer
- Customer type: Registered customers and wholesale-oriented buyers

The original dataset contains transaction information including:

- Invoice number
- Stock code
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

Dataset source:

https://archive.ics.uci.edu/dataset/502/online%2Bretail%2Bii

---

## Project Workflow

```text
Raw Transaction Data
        ↓
Python Data Cleaning
        ↓
PostgreSQL Database
        ↓
SQL Analysis
        ↓
Customer RFM Analysis
        ↓
Product Analysis
        ↓
Streamlit Dashboard
        ↓
Business Insights & Recommendations
