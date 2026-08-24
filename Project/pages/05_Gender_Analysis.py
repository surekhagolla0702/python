import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Gender Analysis",
    page_icon="👥",
    layout="wide"
)

st.title("Gender Analysis")

st.write(
    "Compare credit characteristics across genders."
)


# ---------------- LOAD DATASET ----------------

df = pd.read_csv("data/application_train.csv")


# ---------------- SIDEBAR FILTER ----------------

st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df["CODE_GENDER"].dropna().unique(),
    default=df["CODE_GENDER"].dropna().unique()
)


# ---------------- APPLY FILTER ----------------

df_filtered = df[
    df["CODE_GENDER"].isin(gender)
]


if df_filtered.empty:
    st.warning("No customers available for the selected filters.")
    st.stop()


# ---------------- KPI CALCULATIONS ----------------

male_applicants = (
    df_filtered["CODE_GENDER"] == "M"
).sum()

female_applicants = (
    df_filtered["CODE_GENDER"] == "F"
).sum()

male_default_rate = (
    df_filtered.loc[
        df_filtered["CODE_GENDER"] == "M",
        "TARGET"
    ].mean() * 100
)

female_default_rate = (
    df_filtered.loc[
        df_filtered["CODE_GENDER"] == "F",
        "TARGET"
    ].mean() * 100
)


# ---------------- KPI CARDS ----------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Male Applicants",
    f"{male_applicants:,}"
)

col2.metric(
    "Female Applicants",
    f"{female_applicants:,}"
)

col3.metric(
    "Male Default Rate",
    f"{male_default_rate:.2f}%"
)

col4.metric(
    "Female Default Rate",
    f"{female_default_rate:.2f}%"
)


# ---------------- APPLICANTS BY GENDER ----------------

st.subheader("Applicants by Gender")

gender_customers = (
    df_filtered["CODE_GENDER"]
    .value_counts()
    .rename(
        index={
            "M": "Male",
            "F": "Female"
        }
    )
    .reset_index()
)

gender_customers.columns = [
    "Gender",
    "Customers"
]

st.bar_chart(
    gender_customers,
    x="Gender",
    y="Customers"
)


# ---------------- DEFAULT CUSTOMERS BY GENDER ----------------

st.subheader("Default Customers by Gender")

default_gender = (
    df_filtered[
        df_filtered["TARGET"] == 1
    ]["CODE_GENDER"]
    .value_counts()
    .rename(
        index={
            "M": "Male",
            "F": "Female"
        }
    )
    .reset_index()
)

default_gender.columns = [
    "Gender",
    "Defaults"
]

st.bar_chart(
    default_gender,
    x="Gender",
    y="Defaults"
)


# ---------------- DEFAULT RATE BY GENDER ----------------

st.subheader("Default Rate by Gender")

default_rate_gender = (
    df_filtered
    .groupby("CODE_GENDER")["TARGET"]
    .mean()
    .reset_index()
)

default_rate_gender["Gender"] = (
    default_rate_gender["CODE_GENDER"]
    .map({
        "M": "Male",
        "F": "Female"
    })
)

default_rate_gender["Default Rate (%)"] = (
    default_rate_gender["TARGET"] * 100
)

st.bar_chart(
    default_rate_gender,
    x="Gender",
    y="Default Rate (%)"
)


# ---------------- AVERAGE INCOME BY GENDER ----------------

st.subheader("Average Income by Gender")

income_gender = (
    df_filtered
    .groupby("CODE_GENDER")["AMT_INCOME_TOTAL"]
    .mean()
    .reset_index()
)

income_gender["Gender"] = (
    income_gender["CODE_GENDER"]
    .map({
        "M": "Male",
        "F": "Female"
    })
)

income_gender.columns = [
    "Code",
    "Average Income",
    "Gender"
]

st.bar_chart(
    income_gender,
    x="Gender",
    y="Average Income"
)


# ---------------- AVERAGE CREDIT BY GENDER ----------------

st.subheader("Average Credit by Gender")

credit_gender = (
    df_filtered
    .groupby("CODE_GENDER")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

credit_gender["Gender"] = (
    credit_gender["CODE_GENDER"]
    .map({
        "M": "Male",
        "F": "Female"
    })
)

credit_gender.columns = [
    "Code",
    "Average Credit",
    "Gender"
]

st.bar_chart(
    credit_gender,
    x="Gender",
    y="Average Credit"
)


# ---------------- AVERAGE ANNUITY BY GENDER ----------------

st.subheader("Average Annuity by Gender")

annuity_gender = (
    df_filtered
    .groupby("CODE_GENDER")["AMT_ANNUITY"]
    .mean()
    .reset_index()
)

annuity_gender["Gender"] = (
    annuity_gender["CODE_GENDER"]
    .map({
        "M": "Male",
        "F": "Female"
    })
)

annuity_gender.columns = [
    "Code",
    "Average Annuity",
    "Gender"
]

st.bar_chart(
    annuity_gender,
    x="Gender",
    y="Average Annuity"
)


# ---------------- COMPARISON TABLE ----------------

st.subheader("Gender Comparison Table")

comparison = (
    df_filtered
    .groupby("CODE_GENDER")
    .agg(
        Customers=("CODE_GENDER", "size"),
        Defaults=("TARGET", "sum"),
        Default_Rate=("TARGET", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean")
    )
    .reset_index()
)

comparison["Gender"] = (
    comparison["CODE_GENDER"]
    .map({
        "M": "Male",
        "F": "Female"
    })
)

comparison["Default Rate"] = (
    comparison["Default_Rate"] * 100
)

comparison = comparison[
    [
        "Gender",
        "Customers",
        "Defaults",
        "Default Rate",
        "Avg_Income",
        "Avg_Credit"
    ]
]

comparison = comparison.rename(
    columns={
        "Avg_Income": "Avg Income",
        "Avg_Credit": "Avg Credit"
    }
)

st.dataframe(
    comparison,
    use_container_width=True
)


# ---------------- ADDITIONAL INFORMATION ----------------

st.subheader("Additional Information")

highest_default_gender = (
    comparison
    .loc[comparison["Default Rate"].idxmax()]
)

highest_income_gender = (
    comparison
    .loc[comparison["Avg Income"].idxmax()]
)

highest_credit_gender = (
    comparison
    .loc[comparison["Avg Credit"].idxmax()]
)

st.write(
    "Highest Default Rate:",
    f"{highest_default_gender['Gender']} "
    f"({highest_default_gender['Default Rate']:.2f}%)"
)

st.write(
    "Highest Average Income:",
    f"{highest_income_gender['Gender']} "
    f"({highest_income_gender['Avg Income']:,.0f})"
)

st.write(
    "Highest Average Credit:",
    f"{highest_credit_gender['Gender']} "
    f"({highest_credit_gender['Avg Credit']:,.0f})"
)
