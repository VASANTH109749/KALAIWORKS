import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Mobile Sales Dashboard", layout="wide")

st.title("📱 Mobile Sales Data Dashboard")

# ----------------------------
# Create Dummy Dataset
# ----------------------------

np.random.seed(42)

cities = ["Chennai", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Kolkata"]
latitudes = [13.0827, 19.0760, 28.7041, 12.9716, 17.3850, 22.5726]
longitudes = [80.2707, 72.8777, 77.1025, 77.5946, 78.4867, 88.3639]

models = ["iPhone SE", "OnePlus Nord", "Galaxy Note 20"]
payments = ["UPI", "Debit Card", "Credit Card", "Cash"]

dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(30)]

data = []

for _ in range(500):
    city_index = np.random.randint(0, len(cities))
    data.append([
        np.random.choice(dates),
        cities[city_index],
        latitudes[city_index],
        longitudes[city_index],
        np.random.choice(models),
        np.random.choice(payments),
        np.random.randint(10000, 80000),
        np.random.randint(1, 5),
        np.random.randint(1, 6)
    ])

df = pd.DataFrame(data, columns=[
    "Date", "City", "Latitude", "Longitude",
    "Model", "Payment", "Sales", "Quantity", "Rating"
])

# ----------------------------
# Sidebar Filters
# ----------------------------

st.sidebar.header("Filters")

selected_city = st.sidebar.multiselect(
    "Select City",
    df["City"].unique(),
    default=df["City"].unique()
)

selected_model = st.sidebar.multiselect(
    "Select Model",
    df["Model"].unique(),
    default=df["Model"].unique()
)

filtered_df = df[
    (df["City"].isin(selected_city)) &
    (df["Model"].isin(selected_model))
]

# ----------------------------
# KPI Cards
# ----------------------------

total_sales = filtered_df["Sales"].sum()
total_transactions = len(filtered_df)
avg_rating = round(filtered_df["Rating"].mean(), 2)
total_quantity = filtered_df["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"₹{total_sales:,}")
col2.metric("🧾 Transactions", total_transactions)
col3.metric("⭐ Avg Rating", avg_rating)
col4.metric("📦 Quantity Sold", total_quantity)

st.markdown("---")

# ----------------------------
# Row 1: Daily Trend
# ----------------------------

daily_sales = filtered_df.groupby("Date")["Quantity"].sum().reset_index()

fig_trend = px.line(
    daily_sales,
    x="Date",
    y="Quantity",
    title="Total Quantity by Day"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ----------------------------
# Row 2: Map + Model Sales
# ----------------------------

col5, col6 = st.columns(2)

# Map
city_sales = filtered_df.groupby(["City", "Latitude", "Longitude"])["Sales"].sum().reset_index()

fig_map = px.scatter_mapbox(
    city_sales,
    lat="Latitude",
    lon="Longitude",
    size="Sales",
    hover_name="City",
    zoom=4,
    height=400
)

fig_map.update_layout(mapbox_style="open-street-map")

col5.plotly_chart(fig_map, use_container_width=True)

# Model Sales
model_sales = filtered_df.groupby("Model")["Sales"].sum().reset_index()

fig_model = px.bar(
    model_sales,
    x="Model",
    y="Sales",
    title="Total Sales by Mobile Model",
    color="Model"
)

col6.plotly_chart(fig_model, use_container_width=True)

# ----------------------------
# Row 3: Payment + Ratings
# ----------------------------

col7, col8 = st.columns(2)

# Payment
payment_data = filtered_df["Payment"].value_counts().reset_index()
payment_data.columns = ["Payment", "Count"]

fig_payment = px.pie(
    payment_data,
    names="Payment",
    values="Count",
    title="Transactions by Payment Method"
)

col7.plotly_chart(fig_payment, use_container_width=True)

# Ratings
rating_data = filtered_df["Rating"].value_counts().reset_index()
rating_data.columns = ["Rating", "Count"]

fig_rating = px.bar(
    rating_data.sort_values("Rating"),
    x="Rating",
    y="Count",
    title="Customer Ratings"
)

col8.plotly_chart(fig_rating, use_container_width=True)

# ----------------------------
# Row 4: Sales by Day Name
# ----------------------------

filtered_df["DayName"] = filtered_df["Date"].dt.day_name()

day_sales = filtered_df.groupby("DayName")["Sales"].sum().reset_index()

fig_day = px.area(
    day_sales,
    x="DayName",
    y="Sales",
    title="Total Sales by Day Name"
)

st.plotly_chart(fig_day, use_container_width=True)
