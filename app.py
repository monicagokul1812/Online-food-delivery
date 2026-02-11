import streamlit as st
import pandas as pd

# -----------------------
# Load Data
# -----------------------
df = pd.read_csv("cleaned_data.csv")
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Order_Time'] = pd.to_datetime(df['Order_Time']).dt.time

numeric_cols = ['Order_Value', 'Delivery_Time_Min', 'Profit_Margin', 'Discount_Applied', 'Delivery_Rating']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

if 'Cancelled' not in df.columns:
    df['Cancelled'] = 0

# -----------------------
# KPIs
# -----------------------
total_orders = len(df)
total_revenue = df['Order_Value'].sum()
average_order_value = df['Order_Value'].mean()
average_delivery_time = df['Delivery_Time_Min'].mean()
cancellation_rate = (df['Cancelled'].sum() / total_orders) * 100
average_delivery_rating = df['Delivery_Rating'].mean()
profit_margin = (df['Profit_Margin'].sum() / total_revenue) * 100 if total_revenue > 0 else 0

# -----------------------
# Streamlit Layout
# -----------------------
st.set_page_config(page_title="Orders Dashboard", layout="wide")
st.title("*Online Food Delivery Dashboard*")

# KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", f"{total_orders}")
col2.metric("Total Revenue", f"{total_revenue:,.2f}")
col3.metric("Average Order Value", f"{average_order_value:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Average Delivery Time (min)", f"{average_delivery_time:.2f}")
col5.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
col6.metric("Average Delivery Rating", f"{average_delivery_rating:.2f}/5")

st.metric("Profit Margin", f"{profit_margin:.2f}%")

# -----------------------
# Optional Charts
# -----------------------
st.subheader("Revenue by Weekday")
df['Weekday'] = df['Order_Date'].dt.day_name()
revenue_weekday = df.groupby('Weekday')['Order_Value'].sum().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)
st.bar_chart(revenue_weekday)

st.subheader("Orders by Age Group")
bins = [0, 18, 25, 35, 45, 60, 100]
labels = ['<18', '18-25', '26-35', '36-45', '46-60', '60+']
df['Age_Group'] = pd.cut(df['Customer_Age'], bins=bins, labels=labels)
orders_age_group = df.groupby('Age_Group')['Order_ID'].count()
st.bar_chart(orders_age_group)


#  python -m streamlit run app.py