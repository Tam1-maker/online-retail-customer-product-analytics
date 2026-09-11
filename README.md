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

### Dataset Characteristics

* Records: 1,067,371
* Period: December 2009 – December 2011
* Countries: 43
* Variables: 8
* Business type: UK-based online retailer
* Customer type: Registered customers and wholesale-oriented buyers

The original dataset contains transaction information including:

* Invoice number
* Stock code
* Product description
* Quantity
* Invoice date
* Unit price
* Customer ID
* Country

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
```

---

## Key Analysis

### Sales Performance

The analysis examines:

* Revenue trends over time
* Order volume
* Average order value
* Sales performance by period

### Customer Analysis

RFM analysis is used to evaluate customers based on:

* **Recency** — How recently customers purchased
* **Frequency** — How often customers purchased
* **Monetary Value** — How much customers spent

Customers are grouped into meaningful segments to identify high-value customers and potential retention opportunities.

### Product Analysis

Product-level analysis examines:

* Top products by revenue
* Top products by sales volume
* Product contribution to overall sales
* Differences between sales volume and revenue performance

---

## Key Insights

The analysis identifies differences in customer value and product performance that can support targeted business decisions.

Key findings include:

* A relatively small group of high-value customers contributes significantly to overall revenue.
* Customer segments show different purchasing behaviors and therefore require different retention strategies.
* The products with the highest sales volume are not necessarily the products generating the highest revenue.
* Revenue performance varies over time, highlighting periods of stronger and weaker sales activity.

These findings can help the business prioritize high-value customers, improve retention strategies, and optimize product-level decisions.

---

## Dashboard

An interactive Streamlit dashboard was developed to bring the analysis together in a business-friendly format.

The dashboard provides:

* Sales performance overview
* Customer analysis
* RFM customer segmentation
* Product performance analysis
* Interactive filtering and visualization

### Dashboard Preview

![Dashboard Preview](dashboard/dashboard_screenshot.png)

---

## Tools & Technologies

* **Python** — Data cleaning, transformation, RFM analysis and exploratory analysis
* **SQL** — Business analysis and data aggregation
* **PostgreSQL** — Data storage and querying
* **Pandas** — Data manipulation
* **Streamlit** — Interactive dashboard development
* **GitHub** — Version control and project documentation

---

## Project Structure

```text
online-retail-customer-product-analytics/
│
├── sql/
│   └── SQL analysis scripts
│
├── python/
│   └── Python analysis and data processing
│
├── dashboard/
│   ├── README.md
│   └── dashboard_screenshot.png
│
├── README.md
└── .gitignore
```

---

## Business Recommendations

Based on the analysis, the retailer can:

1. **Prioritize high-value customers** through targeted retention campaigns and personalized offers.
2. **Develop differentiated strategies by RFM segment** instead of applying the same approach to all customers.
3. **Review high-volume but lower-revenue products** to evaluate pricing, bundling, and promotional strategies.
4. **Use sales trends to support inventory and marketing planning** during periods of changing demand.

---

## Conclusion

This project demonstrates an end-to-end data analytics workflow, from raw transaction data and data cleaning to SQL analysis, customer segmentation, product analysis, and interactive business reporting.

The project demonstrates practical skills in **Python, SQL, PostgreSQL, customer analytics, RFM segmentation, data visualization, and dashboard development**.
