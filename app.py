import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="*Online Food Delivery Dashboard*",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (Attractive Style)
# -----------------------------
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="online_food_delivery_db"
)

query = "SELECT * FROM online_food_delivery"
df = pd.read_sql(query, conn)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("🔍 Filters")

city = st.sidebar.multiselect(
    "Select City",
    df["City"].unique(),
    default=df["City"].unique()
)

cuisine = st.sidebar.multiselect(
    "Select Cuisine",
    df["Cuisine_Type"].unique(),
    default=df["Cuisine_Type"].unique()
)
df["Order_Day_Type"] = df["Order_Day"].apply(
    lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday"
)
day_type = st.sidebar.multiselect(
    "Order Day Type ",
    df["Order_Day"].unique(),
    default=df["Order_Day"].unique()
)

filtered_df = df[
    (df["City"].isin(city)) &
    (df["Cuisine_Type"].isin(cuisine)) &
    (df["Order_Day"].isin(day_type))
]

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_orders = len(filtered_df)
total_revenue = filtered_df["Final_Amount"].sum()
avg_order_value = filtered_df["Order_Value"].mean()
avg_delivery_time = filtered_df["Delivery_Time_Min"].mean()
cancellation_rate = (
    filtered_df["Order_Status"].eq("Cancelled").sum()
    / total_orders * 100
)
avg_delivery_rating = filtered_df["Delivery_Rating"].mean()
profit_margin = filtered_df["Profit_Margin"].mean()

# -----------------------------
# TITLE
# -----------------------------
st.title("🍔 Online Food Delivery Analytics Dashboard")

# -----------------------------
# KPI ROW
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{total_orders}")
col2.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
col3.metric("Avg Order Value", f"₹ {avg_order_value:.2f}")
col4.metric("Avg Delivery Time", f"{avg_delivery_time:.2f} mins")

col5, col6, col7 = st.columns(3)

col5.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
col6.metric("Avg Delivery Rating", f"{avg_delivery_rating:.2f}")
col7.metric("Profit Margin %", f"{profit_margin:.2f}%")

st.divider()

# -----------------------------
# CHARTS ROW 1
# -----------------------------
col1, col2 = st.columns(2)

# Orders by City
fig_city = px.bar(
    filtered_df.groupby("City")["Order_ID"].count().reset_index(),
    x="City",
    y="Order_ID",
    title="Orders by City",
    color="City"
)
col1.plotly_chart(fig_city, use_container_width=True)

# Monthly Revenue
filtered_df["Month"] = pd.to_datetime(
    filtered_df["Order_Date"]
).dt.to_period("M").astype(str)

fig_month = px.line(
    filtered_df.groupby("Month")["Final_Amount"].sum().reset_index(),
    x="Month",
    y="Final_Amount",
    title="Monthly Revenue Trend",
    markers=True
)
col2.plotly_chart(fig_month, use_container_width=True)

# -----------------------------
# CHARTS ROW 2
# -----------------------------
col1, col2 = st.columns(2)

# Cuisine Performance
fig_cuisine = px.bar(
    filtered_df.groupby("Cuisine_Type")["Order_ID"].count().reset_index(),
    x="Cuisine_Type",
    y="Order_ID",
    title="Cuisine Performance",
    color="Cuisine_Type"
)
col1.plotly_chart(fig_cuisine, use_container_width=True)

# Payment Mode
fig_payment = px.pie(
    filtered_df,
    names="Payment_Mode",
    title="Payment Mode Preference"
)
col2.plotly_chart(fig_payment, use_container_width=True)

# -----------------------------
# CHARTS ROW 3
# -----------------------------
col1, col2 = st.columns(2)

# Delivery Time vs Distance
fig_scatter = px.scatter(
    filtered_df,
    x="Distance_km",
    y="Delivery_Time_Min",
    color="City",
    title="Distance vs Delivery Time"
)
col1.plotly_chart(fig_scatter, use_container_width=True)

# Peak Hour Orders
fig_peak = px.bar(
    filtered_df.groupby("Peak_Hour")["Order_ID"].count().reset_index(),
    x="Peak_Hour",
    y="Order_ID",
    title="Peak Hour Demand",
    color="Peak_Hour"
)
col2.plotly_chart(fig_peak, use_container_width=True)

# -----------------------------
# CHARTS ROW 4
# -----------------------------
col1, col2 = st.columns(2)

# Top Restaurants
top_rest = (
    filtered_df.groupby("Restaurant_Name")["Restaurant_Rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_rest = px.bar(
    top_rest,
    x="Restaurant_Rating",
    y="Restaurant_Name",
    orientation="h",
    title="Top Rated Restaurants"
)
col1.plotly_chart(fig_rest, use_container_width=True)

# Cancellation Reasons
cancel_df = filtered_df[
    filtered_df["Order_Status"] == "Cancelled"
]

fig_cancel = px.bar(
    cancel_df.groupby("Cancellation_Reason")["Order_ID"]
    .count()
    .reset_index(),
    x="Cancellation_Reason",
    y="Order_ID",
    title="Cancellation Reasons",
    color="Cancellation_Reason"
)
col2.plotly_chart(fig_cancel, use_container_width=True)

st.success(" Dashboard Loaded Successfully")