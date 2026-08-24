import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Income Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("Income Analysis")

st.write(
    "Understand customer income and its relationship with credit risk."
)


# ---------------- LOAD DATASET ----------------

df = pd.read_csv("data/application_train.csv")


# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Filters")

education = st.sidebar.multiselect(
    "Education",
    df["NAME_EDUCATION_TYPE"].dropna().unique(),
    default=df["NAME_EDUCATION_TYPE"].dropna().unique()
)

occupation = st.sidebar.multiselect(
    "Occupation",
    df["OCCUPATION_TYPE"].dropna().unique(),
    default=df["OCCUPATION_TYPE"].dropna().unique()
)


# ---------------- APPLY FILTERS ----------------

df_filtered = df[
    (df["NAME_EDUCATION_TYPE"].isin(education)) &
    (df["OCCUPATION_TYPE"].isin(occupation))
]


if df_filtered.empty:
    st.warning("No customers available for the selected filters.")
    st.stop()


# ---------------- KPI CALCULATIONS ----------------

total_income = (
    df_filtered["AMT_INCOME_TOTAL"].sum()
)

average_income = (
    df_filtered["AMT_INCOME_TOTAL"].mean()
)

median_income = (
    df_filtered["AMT_INCOME_TOTAL"].median()
)

maximum_income = (
    df_filtered["AMT_INCOME_TOTAL"].max()
)

average_income_defaulters = (
    df_filtered.loc[
        df_filtered["TARGET"] == 1,
        "AMT_INCOME_TOTAL"
    ].mean()
)


# ---------------- KPI CARDS ----------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Income",
    f"{total_income:,.0f}"
)

col2.metric(
    "Average Income",
    f"{average_income:,.0f}"
)

col3.metric(
    "Median Income",
    f"{median_income:,.0f}"
)

col4.metric(
    "Maximum Income",
    f"{maximum_income:,.0f}"
)

col5.metric(
    "Avg Income of Defaulters",
    f"{average_income_defaulters:,.0f}"
)


# ---------------- INCOME GROUPS ----------------

income_bins = [
    0,
    50000,
    100000,
    150000,
    200000,
    300000,
    500000,
    float("inf")
]

income_labels = [
    "Below 50K",
    "50K–100K",
    "100K–150K",
    "150K–200K",
    "200K–300K",
    "300K–500K",
    "Above 500K"
]

df_filtered["INCOME_GROUP"] = pd.cut(
    df_filtered["AMT_INCOME_TOTAL"],
    bins=income_bins,
    labels=income_labels,
    include_lowest=True,
    right=False
)


# ---------------- INCOME DISTRIBUTION ----------------

st.subheader("Income Distribution")

fig_income = px.histogram(
    df_filtered,
    x="AMT_INCOME_TOTAL",
    nbins=40,
    title="Income Distribution"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ---------------- CUSTOMERS BY INCOME GROUP ----------------

st.subheader("Customers by Income Group")

income_group_count = (
    df_filtered["INCOME_GROUP"]
    .value_counts()
    .reindex(income_labels)
    .reset_index()
)

income_group_count.columns = [
    "Income Group",
    "Customers"
]

st.bar_chart(
    income_group_count,
    x="Income Group",
    y="Customers"
)


# ---------------- DEFAULT RATE BY INCOME GROUP ----------------

st.subheader("Default Rate by Income Group")

income_default = (
    df_filtered
    .groupby(
        "INCOME_GROUP",
        observed=False
    )["TARGET"]
    .mean()
    .reindex(income_labels)
    .reset_index()
)

income_default["Default Rate (%)"] = (
    income_default["TARGET"] * 100
)

income_default.columns = [
    "Income Group",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    income_default,
    x="Income Group",
    y="Default Rate (%)"
)


# ---------------- INCOME VS CREDIT ----------------

st.subheader("Income vs Credit")

fig_credit = px.scatter(
    df_filtered,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    color="TARGET",
    title="Income vs Credit",
    labels={
        "AMT_INCOME_TOTAL": "Income",
        "AMT_CREDIT": "Credit Amount",
        "TARGET": "Default"
    }
)

st.plotly_chart(
    fig_credit,
    use_container_width=True
)


# ---------------- INCOME VS ANNUITY ----------------

st.subheader("Income vs Annuity")

fig_annuity = px.scatter(
    df_filtered,
    x="AMT_INCOME_TOTAL",
    y="AMT_ANNUITY",
    color="TARGET",
    title="Income vs Annuity",
    labels={
        "AMT_INCOME_TOTAL": "Income",
        "AMT_ANNUITY": "Annuity",
        "TARGET": "Default"
    }
)

st.plotly_chart(
    fig_annuity,
    use_container_width=True
)


# ---------------- INCOME BY EDUCATION ----------------

st.subheader("Income by Education")

education_income = (
    df_filtered
    .groupby("NAME_EDUCATION_TYPE")[
        "AMT_INCOME_TOTAL"
    ]
    .mean()
    .reset_index()
)

education_income.columns = [
    "Education",
    "Average Income"
]

st.bar_chart(
    education_income,
    x="Education",
    y="Average Income"
)


# ---------------- INCOME BY OCCUPATION ----------------

st.subheader("Income by Occupation")

occupation_income = (
    df_filtered
    .groupby("OCCUPATION_TYPE")[
        "AMT_INCOME_TOTAL"
    ]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

occupation_income.columns = [
    "Occupation",
    "Average Income"
]

st.bar_chart(
    occupation_income,
    x="Occupation",
    y="Average Income"
)


# ---------------- ADDITIONAL INFORMATION ----------------

st.subheader("Additional Information")

highest_income_group = (
    income_group_count
    .loc[income_group_count["Customers"].idxmax()]
)

highest_risk_income_group = (
    income_default
    .loc[income_default["Default Rate (%)"].idxmax()]
)

highest_income_education = (
    education_income
    .loc[education_income["Average Income"].idxmax()]
)

highest_income_occupation = (
    occupation_income
    .loc[occupation_income["Average Income"].idxmax()]
)

st.write(
    "Average Income:",
    f"{average_income:,.0f}"
)

st.write(
    "Median Income:",
    f"{median_income:,.0f}"
)

st.write(
    "Most Common Income Group:",
    f"{highest_income_group['Income Group']}"
)

st.write(
    "Highest Risk Income Group:",
    f"{highest_risk_income_group['Income Group']} "
    f"({highest_risk_income_group['Default Rate (%)']:.2f}%)"
)

st.write(
    "Highest Average Income Education:",
    f"{highest_income_education['Education']} "
    f"({highest_income_education['Average Income']:,.0f})"
)

st.write(
    "Highest Average Income Occupation:",
    f"{highest_income_occupation['Occupation']} "
    f"({highest_income_occupation['Average Income']:,.0f})"
)
