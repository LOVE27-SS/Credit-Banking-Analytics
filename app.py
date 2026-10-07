import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Credit Banking Analytics", page_icon="💳", layout="wide")

PROJECT_PATH = Path(r"T:\Love\My coding\Credit_Banking_Project")

@st.cache_data
def load_data():
    t = pd.read_csv(PROJECT_PATH / "cleaned_transactions.csv")
    c = pd.read_csv(PROJECT_PATH / "cleaned_customers.csv")

    t["Credit_card"] = pd.to_numeric(t["Credit_card"], errors="coerce").astype("Int64")
    c["C_ID"] = pd.to_numeric(c["C_ID"], errors="coerce").astype("Int64")
    t["Price"] = pd.to_numeric(t["Price"], errors="coerce")
    t["Selling_price"] = pd.to_numeric(t["Selling_price"], errors="coerce")

    df = t.merge(
        c[["C_ID", "Gender", "Age", "City", "State"]],
        left_on="Credit_card",
        right_on="C_ID",
        how="left"
    )

    df["Discount"] = (df["Price"] - df["Selling_price"]).clip(lower=0)
    df["Return_Status"] = df["Return_ind"].map({1: "Returned", 0: "Not Returned"})
    df["Age_Group"] = pd.cut(
        df["Age"], bins=[0, 29, 49, float("inf")],
        labels=["Young", "Mid-age", "Old"]
    )
    df["Order_Hour"] = pd.to_datetime(
        df["Time"].astype(str), errors="coerce"
    ).dt.hour
    median_price = df["Selling_price"].median()
    df["Value_Category"] = df["Selling_price"].apply(
        lambda x: "High-value" if x >= median_price else "Low-value"
    )
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Could not load cleaned CSV files.")
    st.code(str(e))
    st.stop()

st.title("💳 Credit Banking Analytics Dashboard")
st.caption("Interactive visualization of customers, spending, returns and discounts.")

st.sidebar.header("Filters")
states = sorted(df["State"].dropna().unique())
products = sorted(df["P_CATEGORY"].dropna().unique())
payments = sorted(df["Payment_Method"].dropna().unique())

sel_states = st.sidebar.multiselect("State", states, default=states)
sel_products = st.sidebar.multiselect("Product Category", products, default=products)
sel_payments = st.sidebar.multiselect("Payment Method", payments, default=payments)
sel_return = st.sidebar.selectbox("Return Status", ["All", "Returned", "Not Returned"])

data = df[
    df["State"].isin(sel_states) &
    df["P_CATEGORY"].isin(sel_products) &
    df["Payment_Method"].isin(sel_payments)
].copy()

if sel_return != "All":
    data = data[data["Return_Status"] == sel_return]

a, b, c, d = st.columns(4)
a.metric("Transactions", f"{len(data):,}")
b.metric("Total Spending", f"${data['Selling_price'].sum():,.2f}")
c.metric("Total Discount", f"${data['Discount'].sum():,.2f}")
d.metric("Returned Orders", f"{(data['Return_ind'] == 1).sum():,}")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Overview", "👥 Customers", "🛒 Sales", "↩️ Returns", "🏷️ Discounts"]
)

with tab1:
    col1, col2 = st.columns(2)

    category = data.groupby("P_CATEGORY", as_index=False)["Selling_price"].sum().sort_values("Selling_price", ascending=False)
    with col1:
        fig = px.bar(category, x="P_CATEGORY", y="Selling_price",
                     title="Spending by Product Category",
                     labels={"P_CATEGORY": "Product Category", "Selling_price": "Spending"})
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    payment = data.groupby("Payment_Method", as_index=False)["Selling_price"].sum().sort_values("Selling_price", ascending=False)
    with col2:
        fig = px.bar(payment, x="Payment_Method", y="Selling_price",
                     title="Spending by Payment Method",
                     labels={"Payment_Method": "Payment Method", "Selling_price": "Spending"})
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

    state = data.groupby("State", as_index=False)["Selling_price"].sum().sort_values("Selling_price", ascending=False)
    fig = px.bar(state, x="State", y="Selling_price",
                 title="Spending by State",
                 labels={"State": "State", "Selling_price": "Spending"})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    customers = df.drop_duplicates("C_ID").copy()

    seg = customers.groupby(["Gender", "Age_Group"], observed=False).size().reset_index(name="Customers")
    fig = px.bar(seg, x="Age_Group", y="Customers", color="Gender", barmode="group",
                 title="Customer Segmentation by Gender and Age")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        g = customers["Gender"].value_counts().reset_index()
        g.columns = ["Gender", "Customers"]
        fig = px.pie(g, names="Gender", values="Customers", title="Customers by Gender")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        ag = customers["Age_Group"].value_counts().reset_index()
        ag.columns = ["Age_Group", "Customers"]
        fig = px.pie(ag, names="Age_Group", values="Customers", title="Customers by Age Group")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    top = data.groupby("P_CATEGORY", as_index=False)["Selling_price"].sum().sort_values("Selling_price", ascending=False).head(5)
    fig = px.bar(top, x="P_CATEGORY", y="Selling_price",
                 title="Top 5 Product Categories by Spending")
    st.plotly_chart(fig, use_container_width=True)

    value = data.groupby("Value_Category").agg(
        Orders=("Transaction_ID", "count"),
        Spending=("Selling_price", "sum")
    ).reset_index()
    fig = px.bar(value, x="Value_Category", y="Orders", color="Value_Category",
                 title="High-value vs Low-value Orders")
    st.plotly_chart(fig, use_container_width=True)

    hourly = data.groupby("Order_Hour").size().reset_index(name="Orders").sort_values("Order_Hour")
    fig = px.line(hourly, x="Order_Hour", y="Orders", markers=True,
                  title="Orders by Hour",
                  labels={"Order_Hour": "Hour of Day", "Orders": "Orders"})
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    returned = data[data["Return_ind"] == 1]

    state_r = returned.groupby("State").size().reset_index(name="Returns").sort_values("Returns", ascending=False)
    fig = px.bar(state_r, x="State", y="Returns", title="Returns by State")
    st.plotly_chart(fig, use_container_width=True)

    age_r = returned.groupby("Age_Group", observed=False).size().reset_index(name="Returns")
    fig = px.bar(age_r, x="Age_Group", y="Returns", title="Returns by Age Group")
    st.plotly_chart(fig, use_container_width=True)

    condition_r = returned.groupby("Condition").size().reset_index(name="Returns").sort_values("Returns", ascending=False)
    fig = px.bar(condition_r, x="Condition", y="Returns", title="Returns by Product Condition")
    st.plotly_chart(fig, use_container_width=True)

    category_r = returned.groupby("P_CATEGORY").size().reset_index(name="Returns").sort_values("Returns", ascending=False)
    fig = px.bar(category_r, x="P_CATEGORY", y="Returns", title="Returns by Product Category")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    disc = data[data["Discount"] > 0].groupby("Payment_Method")["Discount"].sum().reset_index().sort_values("Discount", ascending=False)
    fig = px.bar(disc, x="Payment_Method", y="Discount",
                 title="Total Discount by Payment Method")
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

    buckets = pd.cut(
        data["Price"] - data["Selling_price"],
        bins=[-float("inf"), 0, 50, 100, float("inf")],
        labels=["No Discount", "Below 50", "50 to 99.99", "100 or More"],
        right=False
    )
    db = buckets.value_counts().reindex(
        ["No Discount", "Below 50", "50 to 99.99", "100 or More"],
        fill_value=0
    ).reset_index()
    db.columns = ["Discount_Bucket", "Orders"]

    fig = px.bar(db, x="Discount_Bucket", y="Orders",
                 title="Discount Amount vs Number of Orders")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Credit Banking Analytics Project | Python + PostgreSQL + Streamlit")
