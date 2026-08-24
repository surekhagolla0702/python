import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Credit Amount Analysis",
    page_icon="💳",
    layout="wide"
)

st.title("Credit Amount Analysis")

st.write(
    "Analyze the amount of credit requested by applicants."
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

total_credit = df["AMT_CREDIT"].sum()
average_credit = df["AMT_CREDIT"].mean()
median_credit = df["AMT_CREDIT"].median()
maximum_credit = df["AMT_CREDIT"].max()
minimum_credit = df["AMT_CREDIT"].min()


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Credit",
    f"{total_credit:,.0f}"
)

col2.metric(
    "Average Credit",
    f"{average_credit:,.0f}"
)

col3.metric(
    "Median Credit",
    f"{median_credit:,.0f}"
)

col4.metric(
    "Maximum Credit",
    f"{maximum_credit:,.0f}"
)

col5.metric(
    "Minimum Credit",
    f"{minimum_credit:,.0f}"
)


# ---------------------------------------------------------
# CREDIT GROUPS
# ---------------------------------------------------------

credit_bins = [
    0,
    100000,
    300000,
    500000,
    700000,
    1000000,
    float("inf")
]

credit_labels = [
    "Below 100K",
    "100K–300K",
    "300K–500K",
    "500K–700K",
    "700K–1M",
    "Above 1M"
]

df["CREDIT_GROUP"] = pd.cut(
    df["AMT_CREDIT"],
    bins=credit_bins,
    labels=credit_labels,
    include_lowest=True,
    right=False
)


# ---------------------------------------------------------
# CREDIT AMOUNT DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Credit Amount Distribution")

fig_distribution = px.histogram(
    df,
    x="AMT_CREDIT",
    nbins=40,
    title="Credit Amount Distribution"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ---------------------------------------------------------
# CREDIT AMOUNT BY TARGET
# ---------------------------------------------------------

st.subheader("Credit Amount by TARGET")

target_credit = (
    df.groupby("TARGET")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

target_credit["TARGET"] = target_credit["TARGET"].map({
    0: "Non-Default",
    1: "Default"
})

fig_target = px.bar(
    target_credit,
    x="TARGET",
    y="AMT_CREDIT",
    title="Average Credit Amount by TARGET",
    text="AMT_CREDIT"
)

st.plotly_chart(
    fig_target,
    use_container_width=True
)


# ---------------------------------------------------------
# AVERAGE CREDIT BY GENDER
# ---------------------------------------------------------

st.subheader("Average Credit by Gender")

gender_credit = (
    df.groupby("CODE_GENDER")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

gender_credit["Gender"] = gender_credit["CODE_GENDER"].map({
    "M": "Male",
    "F": "Female"
})

fig_gender = px.bar(
    gender_credit,
    x="Gender",
    y="AMT_CREDIT",
    title="Average Credit by Gender",
    text="AMT_CREDIT"
)

st.plotly_chart(
    fig_gender,
    use_container_width=True
)


# ---------------------------------------------------------
# CREDIT BY INCOME TYPE
# ---------------------------------------------------------

st.subheader("Credit by Income Type")

income_credit = (
    df.groupby("NAME_INCOME_TYPE")["AMT_CREDIT"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

income_credit.columns = [
    "Income Type",
    "Average Credit"
]

fig_income = px.bar(
    income_credit,
    x="Income Type",
    y="Average Credit",
    title="Average Credit by Income Type",
    text="Average Credit"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ---------------------------------------------------------
# CREDIT BY EDUCATION
# ---------------------------------------------------------

st.subheader("Credit by Education")

education_credit = (
    df.groupby("NAME_EDUCATION_TYPE")["AMT_CREDIT"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

education_credit.columns = [
    "Education",
    "Average Credit"
]

fig_education = px.bar(
    education_credit,
    x="Education",
    y="Average Credit",
    title="Average Credit by Education",
    text="Average Credit"
)

st.plotly_chart(
    fig_education,
    use_container_width=True
)


# ---------------------------------------------------------
# CREDIT BY CONTRACT TYPE
# ---------------------------------------------------------

st.subheader("Credit by Contract Type")

contract_credit = (
    df.groupby("NAME_CONTRACT_TYPE")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

contract_credit.columns = [
    "Contract Type",
    "Average Credit"
]

fig_contract = px.bar(
    contract_credit,
    x="Contract Type",
    y="Average Credit",
    title="Average Credit by Contract Type",
    text="Average Credit"
)

st.plotly_chart(
    fig_contract,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY CREDIT RANGE
# ---------------------------------------------------------

st.subheader("Default Rate by Credit Range")

credit_default = (
    df.groupby("CREDIT_GROUP", observed=False)["TARGET"]
    .mean()
    .reindex(credit_labels)
    .reset_index()
)

credit_default["Default Rate (%)"] = (
    credit_default["TARGET"] * 100
)

fig_default = px.bar(
    credit_default,
    x="CREDIT_GROUP",
    y="Default Rate (%)",
    title="Default Rate by Credit Range",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)
