import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard",
                   layout="wide")

df = pd.read_csv("cleaned_dataset.csv")

# ---------------- KPIs ----------------

total_sales = df["Total_Sales"].sum()

total_orders = df["Order_ID"].count()

customers = df["Customer_ID"].nunique()

avg_order = total_sales / total_orders

revenue_customer = total_sales / customers

st.title("Sales Interactive Dashboard")

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Total Sales", f"${total_sales:,.2f}")
c2.metric("Orders", total_orders)
c3.metric("Customers", customers)
c4.metric("Avg Order Value", f"${avg_order:,.2f}")
c5.metric("Revenue/Customer", f"${revenue_customer:,.2f}")

st.divider()

# Sidebar Filters

city = st.sidebar.multiselect(
    "City",
    df["City"].unique(),
    default=df["City"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered = df[
    (df["City"].isin(city)) &
    (df["Gender"].isin(gender))
]

# ---------------- Charts ----------------

left,right = st.columns(2)

sales_city = filtered.groupby("City")["Total_Sales"].sum().reset_index()

fig = px.bar(
    sales_city,
    x="City",
    y="Total_Sales",
    title="Sales by City"
)

left.plotly_chart(fig,use_container_width=True)

category = filtered.groupby("Category")["Total_Sales"].sum().reset_index()

fig2 = px.pie(
    category,
    names="Category",
    values="Total_Sales",
    title="Sales by Category"
)

right.plotly_chart(fig2,use_container_width=True)

left,right = st.columns(2)

month = filtered.groupby("Month")["Total_Sales"].sum().reset_index()

fig3 = px.line(
    month,
    x="Month",
    y="Total_Sales",
    markers=True,
    title="Monthly Sales"
)

left.plotly_chart(fig3,use_container_width=True)

gender_sales = filtered.groupby("Gender")["Total_Sales"].sum().reset_index()

fig4 = px.bar(
    gender_sales,
    x="Gender",
    y="Total_Sales",
    title="Sales by Gender"
)

right.plotly_chart(fig4,use_container_width=True)

st.divider()

st.subheader("Top 10 Customers")

top = filtered.groupby("Customer_Name")["Total_Sales"]\
.sum().sort_values(ascending=False).head(10)

st.dataframe(top)

fig5 = px.bar(
    top,
    orientation="h",
    title="Top Customers"
)

st.plotly_chart(fig5,use_container_width=True)