import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Contract Type Analysis",
    page_icon="📄",
    layout="wide"
)

st.title("Contract Type Analysis")

st.write(
    "Analyze credit applications according to loan contract type."
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
# KPI CALCULATIONS
# ---------------------------------------------------------

cash_loan_applications = (
    df["NAME_CONTRACT_TYPE"] == "Cash loans"
).sum()

revolving_loan_applications = (
    df["NAME_CONTRACT_TYPE"] == "Revolving loans"
).sum()


cash_loan_default_rate = (
    df.loc[
        df["NAME_CONTRACT_TYPE"] == "Cash loans",
        "TARGET"
    ].mean() * 100
)

revolving_loan_default_rate = (
    df.loc[
        df["NAME_CONTRACT_TYPE"] == "Revolving loans",
        "TARGET"
    ].mean() * 100
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Cash Loan Applications",
    f"{cash_loan_applications:,}"
)

col2.metric(
    "Revolving Loan Applications",
    f"{revolving_loan_applications:,}"
)

col3.metric(
    "Cash Loan Default Rate",
    f"{cash_loan_default_rate:.2f}%"
)

col4.metric(
    "Revolving Loan Default Rate",
    f"{revolving_loan_default_rate:.2f}%"
)


# ---------------------------------------------------------
# APPLICATIONS BY CONTRACT TYPE
# ---------------------------------------------------------

st.subheader("Applications by Contract Type")

contract_count = (
    df["NAME_CONTRACT_TYPE"]
    .value_counts()
    .reset_index()
)

contract_count.columns = [
    "Contract Type",
    "Applications"
]

fig_count = px.bar(
    contract_count,
    x="Contract Type",
    y="Applications",
    title="Applications by Contract Type",
    text="Applications"
)

st.plotly_chart(
    fig_count,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY CONTRACT TYPE
# ---------------------------------------------------------

st.subheader("Default Rate by Contract Type")

contract_default = (
    df.groupby("NAME_CONTRACT_TYPE")["TARGET"]
    .mean()
    .reset_index()
)

contract_default["Default Rate (%)"] = (
    contract_default["TARGET"] * 100
)

fig_default = px.bar(
    contract_default,
    x="NAME_CONTRACT_TYPE",
    y="Default Rate (%)",
    title="Default Rate by Contract Type",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)


# ---------------------------------------------------------
# AVERAGE CREDIT BY CONTRACT TYPE
# ---------------------------------------------------------

st.subheader("Average Credit by Contract Type")

contract_credit = (
    df.groupby("NAME_CONTRACT_TYPE")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

contract_credit.columns = [
    "Contract Type",
    "Average Credit"
]

fig_credit = px.bar(
    contract_credit,
    x="Contract Type",
    y="Average Credit",
    title="Average Credit by Contract Type",
    text="Average Credit"
)

st.plotly_chart(
    fig_credit,
    use_container_width=True
)


# ---------------------------------------------------------
# AVERAGE INCOME BY CONTRACT TYPE
# ---------------------------------------------------------

st.subheader("Average Income by Contract Type")

contract_income = (
    df.groupby("NAME_CONTRACT_TYPE")["AMT_INCOME_TOTAL"]
    .mean()
    .reset_index()
)

contract_income.columns = [
    "Contract Type",
    "Average Income"
]

fig_income = px.bar(
    contract_income,
    x="Contract Type",
    y="Average Income",
    title="Average Income by Contract Type",
    text="Average Income"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ---------------------------------------------------------
# AVERAGE ANNUITY BY CONTRACT TYPE
# ---------------------------------------------------------

st.subheader("Average Annuity by Contract Type")

contract_annuity = (
    df.groupby("NAME_CONTRACT_TYPE")["AMT_ANNUITY"]
    .mean()
    .reset_index()
)

contract_annuity.columns = [
    "Contract Type",
    "Average Annuity"
]

fig_annuity = px.bar(
    contract_annuity,
    x="Contract Type",
    y="Average Annuity",
    title="Average Annuity by Contract Type",
    text="Average Annuity"
)

st.plotly_chart(
    fig_annuity,
    use_container_width=True
)


# ---------------------------------------------------------
# CREDIT-TO-INCOME RATIO BY CONTRACT TYPE
# ---------------------------------------------------------

st.subheader("Credit-to-Income Ratio by Contract Type")

contract_ratio = (
    df.groupby("NAME_CONTRACT_TYPE")[
        "CREDIT_INCOME_RATIO"
    ]
    .mean()
    .reset_index()
)

contract_ratio.columns = [
    "Contract Type",
    "Average Credit-to-Income Ratio"
]

fig_ratio = px.bar(
    contract_ratio,
    x="Contract Type",
    y="Average Credit-to-Income Ratio",
    title="Credit-to-Income Ratio by Contract Type",
    text="Average Credit-to-Income Ratio"
)

st.plotly_chart(
    fig_ratio,
    use_container_width=True
)
