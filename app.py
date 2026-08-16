import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    layout="wide"
)

# Load data
df = pd.read_excel(
    "Nassau Candy Distributor.xlsx",
    sheet_name="Nassau Candy Distributor"
)

# -----------------------------
# Date Range Selector
# -----------------------------

st.subheader("Date Range")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# -----------------------------
# Division Filter
# -----------------------------

division_options = ["All"] + sorted(df["Division"].dropna().unique().tolist())

selected_division = st.selectbox(
    "Select Division",
    division_options
)

# -----------------------------
# Margin Threshold Slider
# -----------------------------

margin_threshold = st.slider(
    "Minimum Gross Margin %",
    min_value=0,
    max_value=100,
    value=5,
    step=5
)

st.write(f"Selected Margin Threshold: {margin_threshold}%")


# -----------------------------
# Product Selection
# -----------------------------

product_options = ["All"] + sorted(
    df["Product Name"].dropna().unique().tolist()
)

selected_product = st.selectbox(
    "Select Product",
    product_options
)


# -----------------------------
# Apply Dashboard Filters
# -----------------------------

filtered_df = df.copy()

# Date filter
if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date) &
        (filtered_df["Order Date"].dt.date <= end_date)
    ]

# Division filter
if selected_division != "All":
    filtered_df = filtered_df[
        filtered_df["Division"] == selected_division]

# Margin filter
margin_data = (
    filtered_df.groupby("Product Name")["Gross Profit"].sum()
    / filtered_df.groupby("Product Name")["Sales"].sum()
    * 100
)

eligible_products = margin_data[
    margin_data >= margin_threshold
    ].index

filtered_df = filtered_df[
    filtered_df["Product Name"].isin(eligible_products)
]        
    

# Product filter
if selected_product != "All":
    filtered_df = filtered_df[
        filtered_df["Product Name"] == selected_product
    ]

st.write("Filtered Records:", len(filtered_df))

# #Sort data by row_ID in asc order
# df=df.sort_values("Row ID",ascending=True)
# df=df.reset_index(drop=True)

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("🍫 Nassau Candy Profitability Dashboard")
st.caption("Product Line Profitability & Margin Performance Analysis")

# --------------------------------
# KPI Calculations
# --------------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()

# Total Cost = Sales - Gross Profit
total_cost = total_sales - total_profit

# Gross Margin %
gross_margin = (total_profit / total_sales) * 100

# Total Units Sold
total_units_sold = filtered_df["Units"].sum()

# Total Products
total_products = filtered_df["Product Name"].nunique()


# --------------------------------
# KPI Cards with Icons
# --------------------------------

st.markdown("""
<style>

.kpi-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    background-color: white;
    min-height: 105px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.kpi-title {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 25px;
    font-weight: 700;
    color: #111827;
}

.kpi-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
}

.sales-icon {
    background: #e8f7ed;
}

.cost-icon {
    background: #fff1f2;
}

.profit-icon {
    background: #eaf8ee;
}

.margin-icon {
    background: #f3eefe;
}

.units-icon {
    background: #eaf5ff;
}

.products-icon {
    background: #fff3e6;
}

</style>
""", unsafe_allow_html=True)


# Six KPI columns
col1, col2, col3, col4, col5, col6 = st.columns(6)


# Total Sales
with col1:
    st.markdown(f"""
    <div class="kpi-container">
        <div>
            <div class="kpi-title">Total Sales</div>
            <div class="kpi-value">${total_sales:,.0f}</div>
        </div>
        <div class="kpi-icon sales-icon">💵</div>
    </div>
    """, unsafe_allow_html=True)


# Total Cost
with col2:
    st.markdown(f"""
    <div class="kpi-container">
        <div>
            <div class="kpi-title">Total Cost</div>
            <div class="kpi-value">${total_cost:,.0f}</div>
        </div>
        <div class="kpi-icon cost-icon">🏷️</div>
    </div>
    """, unsafe_allow_html=True)


# Gross Profit
with col3:
    st.markdown(f"""
    <div class="kpi-container">
        <div>
            <div class="kpi-title">Total Gross Profit</div>
            <div class="kpi-value">${total_profit:,.0f}</div>
        </div>
        <div class="kpi-icon profit-icon">📈</div>
    </div>
    """, unsafe_allow_html=True)


# Gross Margin
with col4:
    st.markdown(f"""
    <div class="kpi-container">
        <div>
            <div class="kpi-title">Gross Margin</div>
            <div class="kpi-value">{gross_margin:.2f}%</div>
        </div>
        <div class="kpi-icon margin-icon">%</div>
    </div>
    """, unsafe_allow_html=True)


# Total Units Sold
with col5:
    st.markdown(f"""
    <div class="kpi-container">
        <div>
            <div class="kpi-title">Total Units Sold</div>
            <div class="kpi-value">{total_units_sold:,.0f}</div>
        </div>
        <div class="kpi-icon units-icon">📦</div>
    </div>
    """, unsafe_allow_html=True)


# Total Products
with col6:
    st.markdown(f"""
    <div class="kpi-container">
        <div>
            <div class="kpi-title">Total Products</div>
            <div class="kpi-value">{total_products}</div>
        </div>
        <div class="kpi-icon products-icon">🛍️</div>
    </div>
    """, unsafe_allow_html=True)


st.divider()

# -----------------------------
# Data Preview
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(16), use_container_width=True)




# -----------------------------
# Product Profitability Overview
# -----------------------------

st.subheader("Product Profitability Overview")

product_summary = (
    filtered_df.groupby("Product Name", as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Gross_Profit=("Gross Profit", "sum")
      )
)

product_summary["Gross Margin %"] = (
    product_summary["Gross_Profit"] /
    product_summary["Sales"] * 100
)

product_summary = product_summary.sort_values(
    "Gross Margin %",
    ascending=False
)

st.dataframe(
    product_summary,
    use_container_width=True
)

# -----------------------------
# Top 10 Products by Gross Profit
# -----------------------------

st.subheader("Top 10 Products by Gross Profit")

top_products = product_summary.sort_values(
    "Gross_Profit",
    ascending=False).head(10)

st.bar_chart(
    top_products.set_index("Product Name")["Gross_Profit"]
)

# -----------------------------
# Revenue vs Gross Profit
# -----------------------------

st.subheader("Revenue vs Gross Profit")

top_revenue = (
    product_summary
    .sort_values("Sales", ascending=False)
    .head(10)
)

st.bar_chart(
    top_revenue.set_index("Product Name")[["Sales", "Gross_Profit"]]
)

# -----------------------------
# Gross Margin Leaderboard
# -----------------------------

st.subheader("Top 10 Products by Gross Margin")

top_margin = (
    product_summary
    .sort_values("Gross Margin %", ascending=False)
    .head(10)
)

st.bar_chart(
    top_margin.set_index("Product Name")["Gross Margin %"]
)

# -----------------------------
# Profit Contribution Chart
# -----------------------------

st.subheader("Profit Contribution by Product")

profit_contribution = (
    product_summary
    .sort_values("Gross_Profit", ascending=False)
    .head(10)
)

st.bar_chart(
    profit_contribution.set_index("Product Name")["Gross_Profit"]
)

# -----------------------------
# Division Performance Dashboard
# -----------------------------

st.subheader("Revenue vs Profit by Division")

division_summary = (
    filtered_df.groupby("Division", as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Gross_Profit=("Gross Profit", "sum")
      )
)

st.bar_chart(
    division_summary.set_index("Division")[["Sales", "Gross_Profit"]]
)


# -----------------------------
# Margin % by Division
# -----------------------------

st.subheader("Gross Margin % by Division")

division_margin = (
    filtered_df.groupby("Division", as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Gross_Profit=("Gross Profit", "sum")
      )
)

division_margin["Gross Margin %"] = (
    division_margin["Gross_Profit"] /
    division_margin["Sales"] * 100
)

st.bar_chart(
    division_margin.set_index("Division")["Gross Margin %"]
)


# -----------------------------
# Cost vs Sales Diagnostic
# -----------------------------

st.subheader("Cost vs Sales")

cost_sales = (
    filtered_df.groupby("Product Name", as_index=False)
      .agg(
          Cost=("Cost", "sum"),
          Sales=("Sales", "sum")
      )
)

st.scatter_chart(
    cost_sales,
    x="Cost",
    y="Sales"
)


# -----------------------------
# Margin Risk Flags
# -----------------------------

st.subheader("Margin Risk Flags")

risk_data = (
    filtered_df.groupby("Product Name", as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Gross_Profit=("Gross Profit", "sum")
      )
)

risk_data["Gross Margin %"] = (
    risk_data["Gross_Profit"] /
    risk_data["Sales"] * 100
)

risk_data["Risk Flag"] = risk_data["Gross Margin %"].apply(
    lambda x: "High Risk" if x <= 20
    else "Medium Risk" if x <= 40
    else "Low Risk"
)

st.dataframe(
    risk_data.sort_values("Gross Margin %"),
    use_container_width=True
)


# -----------------------------
# Profit Concentration Analysis
# -----------------------------

st.subheader("Profit Concentration - Pareto Analysis")

pareto = (
    filtered_df.groupby("Product Name", as_index=False)
      .agg(Gross_Profit=("Gross Profit", "sum"))
      .sort_values("Gross_Profit", ascending=False)
)

pareto["Profit Contribution %"] = (
    pareto["Gross_Profit"] /
    pareto["Gross_Profit"].sum() * 100
)

pareto["Cumulative Profit %"] = (
    pareto["Profit Contribution %"].cumsum()
)

st.dataframe(
    pareto,
    use_container_width=True
)

# -----------------------------
# Pareto Chart
# -----------------------------

st.subheader("Cumulative Profit Contribution")

st.line_chart(
    pareto.set_index("Product Name")["Cumulative Profit %"]
)

# -----------------------------
# Dependency Indicators
# -----------------------------

st.subheader("Profit Dependency Indicators")

total_profit = product_summary["Gross_Profit"].sum()

top_10_profit = (
    product_summary
    .sort_values("Gross_Profit", ascending=False)
    .head(10)["Gross_Profit"]
    .sum()
)

top_10_dependency = (top_10_profit / total_profit) * 100

st.metric(
    "Top 10 Products Profit Dependency",
    f"{top_10_dependency:.2f}%"
)







