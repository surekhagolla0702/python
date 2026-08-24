import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Education Analysis",
    page_icon="🎓",
    layout="wide"
)

st.title("Education Analysis")

st.write(
    "Analyze applicants according to education level."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)
df = create_features(df)


# ---------------------------------------------------------
# CREDIT-TO-INCOME RATIO
# ---------------------------------------------------------

df["CREDIT_INCOME_RATIO"] = (
    df["AMT_CREDIT"] /
    df["AMT_INCOME_TOTAL"]
)

df["CREDIT_INCOME_RATIO"] = (
    df["CREDIT_INCOME_RATIO"]
    .replace(
        [float("inf"), -float("inf")],
        pd.NA
    )
)


# ---------------------------------------------------------
# EDUCATION SUMMARY
# ---------------------------------------------------------

education_summary = (
    df.groupby("NAME_EDUCATION_TYPE")
    .agg(
        Customers=("TARGET", "size"),
        Default_Rate=("TARGET", "mean"),
        Average_Income=(
            "AMT_INCOME_TOTAL",
            "mean"
        ),
        Average_Credit=(
            "AMT_CREDIT",
            "mean"
        ),
        Average_Annuity=(
            "AMT_ANNUITY",
            "mean"
        ),
        Average_Credit_Income_Ratio=(
            "CREDIT_INCOME_RATIO",
            "mean"
        )
    )
    .reset_index()
)


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

most_common_education = (
    df["NAME_EDUCATION_TYPE"]
    .mode()[0]
)

highest_income_education = (
    education_summary.loc[
        education_summary[
            "Average_Income"
        ].idxmax(),
        "NAME_EDUCATION_TYPE"
    ]
)

lowest_default_education = (
    education_summary.loc[
        education_summary[
            "Default_Rate"
        ].idxmin(),
        "NAME_EDUCATION_TYPE"
    ]
)

highest_default_education = (
    education_summary.loc[
        education_summary[
            "Default_Rate"
        ].idxmax(),
        "NAME_EDUCATION_TYPE"
    ]
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Most Common Education",
    most_common_education
)

col2.metric(
    "Highest Income Education Group",
    highest_income_education
)

col3.metric(
    "Lowest Default Education Group",
    lowest_default_education
)

col4.metric(
    "Highest Default Education Group",
    highest_default_education
)


# ---------------------------------------------------------
# CUSTOMERS BY EDUCATION
# ---------------------------------------------------------

st.subheader("Customers by Education")

education_count = (
    df["NAME_EDUCATION_TYPE"]
    .value_counts()
    .reset_index()
)

education_count.columns = [
    "Education",
    "Customers"
]

fig_customers = px.bar(
    education_count,
    x="Education",
    y="Customers",
    title="Customers by Education",
    text="Customers"
)

st.plotly_chart(
    fig_customers,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY EDUCATION
# ---------------------------------------------------------

st.subheader("Default Rate by Education")

default_education = (
    education_summary.copy()
)

default_education["Default Rate (%)"] = (
    default_education["Default_Rate"] * 100
)

fig_default = px.bar(
    default_education,
    x="NAME_EDUCATION_TYPE",
    y="Default Rate (%)",
    title="Default Rate by Education",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)


# ---------------------------------------------------------
# INCOME BY EDUCATION
# ---------------------------------------------------------

st.subheader("Income by Education")

fig_income = px.bar(
    education_summary,
    x="NAME_EDUCATION_TYPE",
    y="Average_Income",
    title="Average Income by Education",
    text="Average_Income"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ---------------------------------------------------------
# CREDIT BY EDUCATION
# ---------------------------------------------------------

st.subheader("Credit by Education")

fig_credit = px.bar(
    education_summary,
    x="NAME_EDUCATION_TYPE",
    y="Average_Credit",
    title="Average Credit by Education",
    text="Average_Credit"
)

st.plotly_chart(
    fig_credit,
    use_container_width=True
)


# ---------------------------------------------------------
# ANNUITY BY EDUCATION
# ---------------------------------------------------------

st.subheader("Annuity by Education")

fig_annuity = px.bar(
    education_summary,
    x="NAME_EDUCATION_TYPE",
    y="Average_Annuity",
    title="Average Annuity by Education",
    text="Average_Annuity"
)

st.plotly_chart(
    fig_annuity,
    use_container_width=True
)

# ---------------------------------------------------------
# CREDIT-TO-INCOME RATIO BY EDUCATION
# ---------------------------------------------------------

st.subheader("Credit-to-Income Ratio by Education")

fig_ratio = px.bar(
    education_summary,
    x="NAME_EDUCATION_TYPE",
    y="Average_Credit_Income_Ratio",
    title="Credit-to-Income Ratio by Education",
    text="Average_Credit_Income_Ratio"
)

st.plotly_chart(
    fig_ratio,
    use_container_width=True
)
