import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Family & Children Analysis",
    page_icon="👨‍👩‍👧‍👦",
    layout="wide"
)

st.title("Family & Children Analysis")

st.write(
    "Study whether household characteristics influence credit risk."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)
df = create_features(df)


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

average_children = (
    df["CNT_CHILDREN"].mean()
)

average_family_members = (
    df["CNT_FAM_MEMBERS"].mean()
)

customers_with_children = (
    df["CNT_CHILDREN"] > 0
).sum()

customers_without_children = (
    df["CNT_CHILDREN"] == 0
).sum()


# Highest risk family type

family_risk = (
    df.dropna(subset=["NAME_FAMILY_STATUS"])
    .groupby("NAME_FAMILY_STATUS")["TARGET"]
    .mean()
    .sort_values(ascending=False)
)

if len(family_risk) > 0:
    highest_risk_family_type = family_risk.index[0]
else:
    highest_risk_family_type = "N/A"


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Average Children",
    f"{average_children:.2f}"
)

col2.metric(
    "Average Family Members",
    f"{average_family_members:.2f}"
)

col3.metric(
    "Customers with Children",
    f"{customers_with_children:,}"
)

col4.metric(
    "Customers without Children",
    f"{customers_without_children:,}"
)

col5.metric(
    "Highest Risk Family Type",
    highest_risk_family_type
)


# ---------------------------------------------------------
# CUSTOMERS BY NUMBER OF CHILDREN
# ---------------------------------------------------------

st.subheader("Customers by Number of Children")

children_count = (
    df["CNT_CHILDREN"]
    .value_counts()
    .sort_index()
    .reset_index()
)

children_count.columns = [
    "Number of Children",
    "Customers"
]

fig_children = px.bar(
    children_count,
    x="Number of Children",
    y="Customers",
    title="Customers by Number of Children",
    text="Customers"
)

st.plotly_chart(
    fig_children,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY NUMBER OF CHILDREN
# ---------------------------------------------------------

st.subheader("Default Rate by Number of Children")

children_default = (
    df.groupby("CNT_CHILDREN")["TARGET"]
    .mean()
    .reset_index()
)

children_default["Default Rate (%)"] = (
    children_default["TARGET"] * 100
)

fig_children_default = px.bar(
    children_default,
    x="CNT_CHILDREN",
    y="Default Rate (%)",
    title="Default Rate by Number of Children",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_children_default,
    use_container_width=True
)


# ---------------------------------------------------------
# CUSTOMERS BY FAMILY SIZE
# ---------------------------------------------------------

st.subheader("Customers by Family Size")

family_size = (
    df["CNT_FAM_MEMBERS"]
    .value_counts()
    .sort_index()
    .reset_index()
)

family_size.columns = [
    "Family Size",
    "Customers"
]

fig_family_size = px.bar(
    family_size,
    x="Family Size",
    y="Customers",
    title="Customers by Family Size",
    text="Customers"
)

st.plotly_chart(
    fig_family_size,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY FAMILY SIZE
# ---------------------------------------------------------

st.subheader("Default Rate by Family Size")

family_default = (
    df.groupby("CNT_FAM_MEMBERS")["TARGET"]
    .mean()
    .reset_index()
)

family_default["Default Rate (%)"] = (
    family_default["TARGET"] * 100
)

fig_family_default = px.bar(
    family_default,
    x="CNT_FAM_MEMBERS",
    y="Default Rate (%)",
    title="Default Rate by Family Size",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_family_default,
    use_container_width=True
)


# ---------------------------------------------------------
# APPLICATIONS BY FAMILY STATUS
# ---------------------------------------------------------

st.subheader("Applications by Family Status")

family_status_count = (
    df["NAME_FAMILY_STATUS"]
    .dropna()
    .value_counts()
    .reset_index()
)

family_status_count.columns = [
    "Family Status",
    "Applications"
]

fig_family_status = px.bar(
    family_status_count,
    x="Family Status",
    y="Applications",
    title="Applications by Family Status",
    text="Applications"
)

st.plotly_chart(
    fig_family_status,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY FAMILY STATUS
# ---------------------------------------------------------

st.subheader("Default Rate by Family Status")

family_status_default = (
    df.dropna(subset=["NAME_FAMILY_STATUS"])
    .groupby("NAME_FAMILY_STATUS")["TARGET"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

family_status_default["Default Rate (%)"] = (
    family_status_default["TARGET"] * 100
)

fig_family_status_default = px.bar(
    family_status_default,
    x="NAME_FAMILY_STATUS",
    y="Default Rate (%)",
    title="Default Rate by Family Status",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_family_status_default,
    use_container_width=True
)


# ---------------------------------------------------------
# INCOME VS FAMILY SIZE
# ---------------------------------------------------------

st.subheader("Income vs Family Size")

income_family = (
    df.groupby("CNT_FAM_MEMBERS")["AMT_INCOME_TOTAL"]
    .mean()
    .reset_index()
)

income_family.columns = [
    "Family Size",
    "Average Income"
]

fig_income_family = px.bar(
    income_family,
    x="Family Size",
    y="Average Income",
    title="Average Income vs Family Size",
    text="Average Income"
)

st.plotly_chart(
    fig_income_family,
    use_container_width=True
)
