import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Target / Default Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("Target / Default Analysis")

st.write("Analyze the main TARGET variable.")


# ---------------- LOAD DATASET ----------------

df = pd.read_csv("data/application_train.csv")


# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df["CODE_GENDER"].dropna().unique(),
    default=df["CODE_GENDER"].dropna().unique()
)

income_type = st.sidebar.multiselect(
    "Income Type",
    df["NAME_INCOME_TYPE"].dropna().unique(),
    default=df["NAME_INCOME_TYPE"].dropna().unique()
)

education = st.sidebar.multiselect(
    "Education",
    df["NAME_EDUCATION_TYPE"].dropna().unique(),
    default=df["NAME_EDUCATION_TYPE"].dropna().unique()
)

contract_type = st.sidebar.multiselect(
    "Contract Type",
    df["NAME_CONTRACT_TYPE"].dropna().unique(),
    default=df["NAME_CONTRACT_TYPE"].dropna().unique()
)


# ---------------- APPLY FILTERS ----------------

df_filtered = df[
    (df["CODE_GENDER"].isin(gender)) &
    (df["NAME_INCOME_TYPE"].isin(income_type)) &
    (df["NAME_EDUCATION_TYPE"].isin(education)) &
    (df["NAME_CONTRACT_TYPE"].isin(contract_type))
]


# ---------------- CHECK FILTERED DATA ----------------

if df_filtered.empty:
    st.warning("No customers available for the selected filters.")
    st.stop()


# ---------------- KPI CALCULATIONS ----------------

total_customers = len(df_filtered)

target_0 = (
    df_filtered["TARGET"] == 0
).sum()

target_1 = (
    df_filtered["TARGET"] == 1
).sum()

default_rate = (
    target_1 / total_customers * 100
    if total_customers != 0
    else 0
)

non_default_rate = (
    target_0 / total_customers * 100
    if total_customers != 0
    else 0
)


# ---------------- KPI CARDS ----------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "TARGET = 0 Customers",
    f"{target_0:,}"
)

col2.metric(
    "TARGET = 1 Customers",
    f"{target_1:,}"
)

col3.metric(
    "Default Rate %",
    f"{default_rate:.2f}%"
)

col4.metric(
    "Non-Default Rate %",
    f"{non_default_rate:.2f}%"
)


# ---------------- TARGET COUNT BAR CHART ----------------

st.subheader("TARGET Count Bar Chart")

target_count = (
    df_filtered["TARGET"]
    .value_counts()
    .sort_index()
    .reset_index()
)

target_count.columns = [
    "TARGET",
    "Customers"
]

target_count["TARGET"] = target_count["TARGET"].map({
    0: "TARGET = 0",
    1: "TARGET = 1"
})

st.bar_chart(
    target_count,
    x="TARGET",
    y="Customers"
)


# ---------------- TARGET PERCENTAGE DONUT CHART ----------------

st.subheader("TARGET Percentage Donut Chart")

fig_target = px.pie(
    target_count,
    names="TARGET",
    values="Customers",
    title="TARGET Percentage Distribution",
    hole=0.45
)

st.plotly_chart(
    fig_target,
    use_container_width=True
)


# ---------------- DEFAULT RATE BY GENDER ----------------

st.subheader("Default Rate by Gender")

default_by_gender = (
    df_filtered
    .groupby("CODE_GENDER")["TARGET"]
    .mean()
    .reset_index()
)

default_by_gender["Default Rate (%)"] = (
    default_by_gender["TARGET"] * 100
)

default_by_gender.columns = [
    "Gender",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_by_gender,
    x="Gender",
    y="Default Rate (%)"
)


# ---------------- DEFAULT RATE BY INCOME TYPE ----------------

st.subheader("Default Rate by Income Type")

default_by_income = (
    df_filtered
    .groupby("NAME_INCOME_TYPE")["TARGET"]
    .mean()
    .reset_index()
)

default_by_income["Default Rate (%)"] = (
    default_by_income["TARGET"] * 100
)

default_by_income.columns = [
    "Income Type",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_by_income,
    x="Income Type",
    y="Default Rate (%)"
)


# ---------------- DEFAULT RATE BY EDUCATION ----------------

st.subheader("Default Rate by Education")

default_by_education = (
    df_filtered
    .groupby("NAME_EDUCATION_TYPE")["TARGET"]
    .mean()
    .reset_index()
)

default_by_education["Default Rate (%)"] = (
    default_by_education["TARGET"] * 100
)

default_by_education.columns = [
    "Education",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_by_education,
    x="Education",
    y="Default Rate (%)"
)


# ---------------- DEFAULT RATE BY CONTRACT TYPE ----------------

st.subheader("Default Rate by Contract Type")

default_by_contract = (
    df_filtered
    .groupby("NAME_CONTRACT_TYPE")["TARGET"]
    .mean()
    .reset_index()
)

default_by_contract["Default Rate (%)"] = (
    default_by_contract["TARGET"] * 100
)

default_by_contract.columns = [
    "Contract Type",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_by_contract,
    x="Contract Type",
    y="Default Rate (%)"
)


# ---------------- ADDITIONAL INFORMATION ----------------

st.subheader("Additional Information")

highest_gender = (
    default_by_gender
    .loc[default_by_gender["Default Rate (%)"].idxmax()]
)

highest_income = (
    default_by_income
    .loc[default_by_income["Default Rate (%)"].idxmax()]
)

highest_education = (
    default_by_education
    .loc[default_by_education["Default Rate (%)"].idxmax()]
)

highest_contract = (
    default_by_contract
    .loc[default_by_contract["Default Rate (%)"].idxmax()]
)

st.write(
    "Overall Default Rate:",
    f"{default_rate:.2f}%"
)

st.write(
    "Overall Non-Default Rate:",
    f"{non_default_rate:.2f}%"
)

st.write(
    "Highest Default Rate by Gender:",
    f"{highest_gender['Gender']} "
    f"({highest_gender['Default Rate (%)']:.2f}%)"
)

st.write(
    "Highest Default Rate by Income Type:",
    f"{highest_income['Income Type']} "
    f"({highest_income['Default Rate (%)']:.2f}%)"
)

st.write(
    "Highest Default Rate by Education:",
    f"{highest_education['Education']} "
    f"({highest_education['Default Rate (%)']:.2f}%)"
)

st.write(
    "Highest Default Rate by Contract Type:",
    f"{highest_contract['Contract Type']} "
    f"({highest_contract['Default Rate (%)']:.2f}%)"
)
