import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Online Retail Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    sales = pd.read_csv(BASE_DIR / "sales_clean.csv", dtype={"Invoice": str})
    monthly = pd.read_csv(BASE_DIR / "monthly_sales.csv")
    customers = pd.read_csv(BASE_DIR / "customer_sales_summary.csv")
    rfm = pd.read_csv(BASE_DIR / "customer_rfm.csv")
    segments = pd.read_csv(BASE_DIR / "customer_segment_summary.csv")
    products = pd.read_csv(BASE_DIR / "product_analysis.csv")
    product_matrix = pd.read_csv(BASE_DIR / "product_value_matrix.csv")

    sales["InvoiceDate"] = pd.to_datetime(sales["InvoiceDate"])

    return sales, monthly, customers, rfm, segments, products, product_matrix
    return (
        sales,
        monthly,
        customers,
        rfm,
        segments,
        products,
        product_matrix
    )


(
    sales,
    monthly,
    customers,
    rfm,
    segments,
    products,
    product_matrix
) = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Online Retail Analytics")

st.sidebar.markdown(
    """
    **Customer & Product Analytics**

    Explore sales performance,
    customer value and product
    performance.
    """
)

page = st.sidebar.radio(
    "Select Analysis",
    [
        "Executive Overview",
        "Customer Analytics",
        "Product Analytics"
    ]
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.title("Online Retail II — Executive Overview")

    st.markdown(
        "Business performance overview based on cleaned transaction data."
    )

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_revenue = sales["Revenue"].sum()
    total_orders = sales["Invoice"].nunique()
    total_customers = sales["Customer ID"].nunique()
    total_products = sales["StockCode"].nunique()
    aov = total_revenue / total_orders

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Revenue",
        f"£{total_revenue / 1_000_000:.2f}M"
    )

    col2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Customers",
        f"{total_customers:,}"
    )

    col4.metric(
        "Products",
        f"{total_products:,}"
    )

    col5.metric(
        "Average Order Value",
        f"£{aov:,.2f}"
    )

    st.divider()

    # --------------------------------------------------------
    # MONTHLY REVENUE
    # --------------------------------------------------------

    st.subheader("Monthly Revenue Trend")

    monthly_chart = px.line(
        monthly,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue"
    )

    monthly_chart.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (£)",
        hovermode="x unified"
    )

    st.plotly_chart(
        monthly_chart,
        use_container_width=True
    )

    # --------------------------------------------------------
    # ORDERS + AOV
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Monthly Orders")

        orders_chart = px.bar(
            monthly,
            x="Month",
            y="Orders",
            title="Monthly Orders"
        )

        orders_chart.update_layout(
            xaxis_title="Month",
            yaxis_title="Orders"
        )

        st.plotly_chart(
            orders_chart,
            use_container_width=True
        )

    with col2:

        st.subheader("Monthly AOV")

        aov_chart = px.line(
            monthly,
            x="Month",
            y="AOV",
            markers=True,
            title="Average Order Value"
        )

        aov_chart.update_layout(
            xaxis_title="Month",
            yaxis_title="AOV (£)"
        )

        st.plotly_chart(
            aov_chart,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    st.subheader("Top 10 Products by Revenue")

    top_products = (
        products
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
        .sort_values(
            "Revenue",
            ascending=True
        )
    )

    product_chart = px.bar(
        top_products,
        x="Revenue",
        y="Description",
        orientation="h",
        title="Top 10 Products by Revenue"
    )

    product_chart.update_layout(
        xaxis_title="Revenue (£)",
        yaxis_title="Product"
    )

    st.plotly_chart(
        product_chart,
        use_container_width=True
    )


# ============================================================
# CUSTOMER ANALYTICS
# ============================================================

elif page == "Customer Analytics":

    st.title("Customer Analytics")

    st.markdown(
        "RFM-based customer segmentation and customer value analysis."
    )

    # --------------------------------------------------------
    # CUSTOMER KPIs
    # --------------------------------------------------------

    total_customer_revenue = customers["Revenue"].sum()

    avg_customer_revenue = customers["Revenue"].mean()

    champions = segments[
        segments["Segment"] == "Champions"
    ]

    at_risk = segments[
        segments["Segment"] == "At Risk"
    ]

    lost = segments[
        segments["Segment"] == "Lost Customers"
    ]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Customers",
        f"{len(customers):,}"
    )

    col2.metric(
        "Avg Customer Revenue",
        f"£{avg_customer_revenue:,.2f}"
    )

    col3.metric(
        "Champions",
        f"{int(champions['Customers'].iloc[0]):,}"
    )

    col4.metric(
        "At Risk + Lost",
        f"{int(at_risk['Customers'].iloc[0] + lost['Customers'].iloc[0]):,}"
    )

    st.divider()

    # --------------------------------------------------------
    # CUSTOMER SEGMENTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Customer Segment Distribution")

        segment_count_chart = px.pie(
            segments,
            names="Segment",
            values="Customers",
            hole=0.45
        )

        st.plotly_chart(
            segment_count_chart,
            use_container_width=True
        )

    with col2:

        st.subheader("Revenue Share by Customer Segment")

        revenue_chart = px.bar(
            segments.sort_values(
                "Revenue",
                ascending=True
            ),
            x="Revenue_Share",
            y="Segment",
            orientation="h"
        )

        revenue_chart.update_layout(
            xaxis_title="Revenue Share (%)",
            yaxis_title="Segment"
        )

        st.plotly_chart(
            revenue_chart,
            use_container_width=True
        )

    # --------------------------------------------------------
    # RFM DISTRIBUTION
    # --------------------------------------------------------

    st.subheader("RFM Distribution")

    col1, col2, col3 = st.columns(3)

    with col1:

        fig_r = px.histogram(
            rfm,
            x="Recency",
            nbins=30,
            title="Recency Distribution"
        )

        st.plotly_chart(
            fig_r,
            use_container_width=True
        )

    with col2:

        fig_f = px.histogram(
            rfm,
            x="Frequency",
            nbins=30,
            title="Frequency Distribution"
        )

        st.plotly_chart(
            fig_f,
            use_container_width=True
        )

    with col3:

        fig_m = px.histogram(
            rfm,
            x="Monetary",
            nbins=30,
            title="Monetary Distribution"
        )

        st.plotly_chart(
            fig_m,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TOP CUSTOMERS
    # --------------------------------------------------------

    st.subheader("Top 10 Customers by Revenue")

    top_customers = (
        customers
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
        .sort_values(
            "Revenue",
            ascending=True
        )
    )

    customer_chart = px.bar(
        top_customers,
        x="Revenue",
        y="Customer ID",
        orientation="h"
    )

    customer_chart.update_layout(
        xaxis_title="Revenue (£)",
        yaxis_title="Customer ID"
    )

    st.plotly_chart(
        customer_chart,
        use_container_width=True
    )


# ============================================================
# PRODUCT ANALYTICS
# ============================================================

elif page == "Product Analytics":

    st.title("Product Analytics")

    st.markdown(
        "Product revenue, sales volume and product value analysis."
    )

    # --------------------------------------------------------
    # PRODUCT KPIs
    # --------------------------------------------------------

    product_revenue = products["Revenue"].sum()

    product_quantity = products["Quantity"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Product Revenue",
        f"£{product_revenue / 1_000_000:.2f}M"
    )

    col2.metric(
        "Units Sold",
        f"{product_quantity:,.0f}"
    )

    col3.metric(
        "Unique Products",
        f"{products['StockCode'].nunique():,}"
    )

    st.divider()

    # --------------------------------------------------------
    # TOP PRODUCTS BY REVENUE
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top 10 Products by Revenue")

        top_revenue = (
            products
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(10)
            .sort_values(
                "Revenue",
                ascending=True
            )
        )

        fig_revenue = px.bar(
            top_revenue,
            x="Revenue",
            y="Description",
            orientation="h"
        )

        fig_revenue.update_layout(
            xaxis_title="Revenue (£)",
            yaxis_title="Product"
        )

        st.plotly_chart(
            fig_revenue,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TOP PRODUCTS BY QUANTITY
    # --------------------------------------------------------

    with col2:

        st.subheader("Top 10 Products by Quantity")

        top_quantity = (
            products
            .sort_values(
                "Quantity",
                ascending=False
            )
            .head(10)
            .sort_values(
                "Quantity",
                ascending=True
            )
        )

        fig_quantity = px.bar(
            top_quantity,
            x="Quantity",
            y="Description",
            orientation="h"
        )

        fig_quantity.update_layout(
            xaxis_title="Quantity Sold",
            yaxis_title="Product"
        )

        st.plotly_chart(
            fig_quantity,
            use_container_width=True
        )

    # --------------------------------------------------------
    # PRODUCT VALUE MATRIX
    # --------------------------------------------------------

    st.subheader("Product Value Matrix")

    fig_matrix = px.scatter(
        product_matrix,
        x="Quantity",
        y="Revenue",
        hover_name="Description",
        hover_data=[
            "StockCode",
            "Orders"
        ],
        log_x=True,
        log_y=True
    )

    fig_matrix.update_layout(
        xaxis_title="Quantity Sold (log scale)",
        yaxis_title="Revenue (£, log scale)"
    )

    st.plotly_chart(
        fig_matrix,
        use_container_width=True
    )

    # --------------------------------------------------------
    # PRODUCT TABLE
    # --------------------------------------------------------

    st.subheader("Top Products")

    display_products = (
        products
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        display_products[
            [
                "StockCode",
                "Description",
                "Quantity",
                "Revenue",
                "Orders",
                "Avg_Price"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )