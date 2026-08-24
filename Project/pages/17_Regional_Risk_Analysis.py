import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Regional Risk Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("Regional Risk Analysis")

st.write(
    "Analyze whether customer location characteristics affect default risk."
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

most_common_region_rating = (
    df["REGION_RATING_CLIENT"]
    .dropna()
    .mode()[0]
)

region_risk = (
    df.groupby("REGION_RATING_CLIENT")["TARGET"]
    .mean()
    .sort_values(ascending=False)
)

highest_risk_region_rating = region_risk.idxmax()

average_population_indicator = (
    df["REGION_POPULATION_RELATIVE"].mean()
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Most Common Region Rating",
    str(most_common_region_rating)
)

col2.metric(
    "Highest Risk Region Rating",
    str(highest_risk_region_rating)
)

col3.metric(
    "Average Regional Population Indicator",
    f"{average_population_indicator:.4f}"
)


# ---------------------------------------------------------
# CUSTOMERS BY REGION RATING
# ---------------------------------------------------------

st.subheader("Customers by Region Rating")

region_count = (
    df["REGION_RATING_CLIENT"]
    .value_counts()
    .sort_index()
    .reset_index()
)

region_count.columns = [
    "Region Rating",
    "Customers"
]

fig_region_count = px.bar(
    region_count,
    x="Region Rating",
    y="Customers",
    title="Customers by Region Rating",
    text="Customers"
)

st.plotly_chart(
    fig_region_count,
    use_container_width=True
)


# ---------------------------------------------------------
# CUSTOMERS BY REGION RATING WITH CITY
# ---------------------------------------------------------

st.subheader("Customers by Region Rating with City")

region_city_count = (
    df["REGION_RATING_CLIENT_W_CITY"]
    .value_counts()
    .sort_index()
    .reset_index()
)

region_city_count.columns = [
    "Region Rating with City",
    "Customers"
]

fig_region_city_count = px.bar(
    region_city_count,
    x="Region Rating with City",
    y="Customers",
    title="Customers by Region Rating with City",
    text="Customers"
)

st.plotly_chart(
    fig_region_city_count,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY REGION RATING
# ---------------------------------------------------------

st.subheader("Default Rate by Region Rating")

region_default = (
    df.groupby("REGION_RATING_CLIENT")["TARGET"]
    .mean()
    .reset_index()
)

region_default["Default Rate (%)"] = (
    region_default["TARGET"] * 100
)

fig_region_default = px.bar(
    region_default,
    x="REGION_RATING_CLIENT",
    y="Default Rate (%)",
    title="Default Rate by Region Rating",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_region_default,
    use_container_width=True
)


# ---------------------------------------------------------
# CREDIT BY REGION RATING
# ---------------------------------------------------------

st.subheader("Credit by Region Rating")

region_credit = (
    df.groupby("REGION_RATING_CLIENT")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

region_credit.columns = [
    "Region Rating",
    "Average Credit"
]

fig_region_credit = px.bar(
    region_credit,
    x="Region Rating",
    y="Average Credit",
    title="Average Credit by Region Rating",
    text="Average Credit"
)

st.plotly_chart(
    fig_region_credit,
    use_container_width=True
)


# ---------------------------------------------------------
# INCOME BY REGION RATING
# ---------------------------------------------------------

st.subheader("Income by Region Rating")

region_income = (
    df.groupby("REGION_RATING_CLIENT")["AMT_INCOME_TOTAL"]
    .mean()
    .reset_index()
)

region_income.columns = [
    "Region Rating",
    "Average Income"
]

fig_region_income = px.bar(
    region_income,
    x="Region Rating",
    y="Average Income",
    title="Average Income by Region Rating",
    text="Average Income"
)

st.plotly_chart(
    fig_region_income,
    use_container_width=True
)


# ---------------------------------------------------------
# REGION MISMATCH VS DEFAULT
# ---------------------------------------------------------

st.subheader("Region Mismatch vs Default")


# 1 = customer does not live/work in the same region
# 0 = customer lives/works in the same region

df["REGION_MISMATCH"] = (
    (df["REG_REGION_NOT_LIVE_REGION"] == 1) |
    (df["REG_REGION_NOT_WORK_REGION"] == 1)
).astype(int)

region_mismatch = (
    df.groupby("REGION_MISMATCH")["TARGET"]
    .mean()
    .reset_index()
)

region_mismatch["Region Mismatch"] = (
    region_mismatch["REGION_MISMATCH"]
    .map({
        0: "No Region Mismatch",
        1: "Region Mismatch"
    })
)

region_mismatch["Default Rate (%)"] = (
    region_mismatch["TARGET"] * 100
)

fig_region_mismatch = px.bar(
    region_mismatch,
    x="Region Mismatch",
    y="Default Rate (%)",
    title="Region Mismatch vs Default",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_region_mismatch,
    use_container_width=True
)


# ---------------------------------------------------------
# CITY MISMATCH VS DEFAULT
# ---------------------------------------------------------

st.subheader("City Mismatch vs Default")


# 1 = customer does not live/work in the same city
# 0 = customer lives/works in the same city

df["CITY_MISMATCH"] = (
    (df["REG_CITY_NOT_LIVE_CITY"] == 1) |
    (df["REG_CITY_NOT_WORK_CITY"] == 1)
).astype(int)

city_mismatch = (
    df.groupby("CITY_MISMATCH")["TARGET"]
    .mean()
    .reset_index()
)

city_mismatch["City Mismatch"] = (
    city_mismatch["CITY_MISMATCH"]
    .map({
        0: "No City Mismatch",
        1: "City Mismatch"
    })
)

city_mismatch["Default Rate (%)"] = (
    city_mismatch["TARGET"] * 100
)

fig_city_mismatch = px.bar(
    city_mismatch,
    x="City Mismatch",
    y="Default Rate (%)",
    title="City Mismatch vs Default",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_city_mismatch,
    use_container_width=True
)


# ---------------------------------------------------------
# REGIONAL SUMMARY TABLE
# ---------------------------------------------------------

st.subheader("Regional Risk Summary")

regional_summary = (
    df.groupby("REGION_RATING_CLIENT")
    .agg(
        Customers=("TARGET", "size"),
        Defaults=("TARGET", "sum"),
        Default_Rate=("TARGET", "mean"),
        Average_Credit=("AMT_CREDIT", "mean"),
        Average_Income=("AMT_INCOME_TOTAL", "mean")
    )
    .reset_index()
)

regional_summary["Default Rate (%)"] = (
    regional_summary["Default_Rate"] * 100
)

st.dataframe(
    regional_summary[
        [
            "REGION_RATING_CLIENT",
            "Customers",
            "Defaults",
            "Default Rate (%)",
            "Average_Credit",
            "Average_Income"
        ]
    ],
    use_container_width=True
)
