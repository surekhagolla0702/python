import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Executive Overview",
    page_icon="🏠",
    layout="wide"
)

st.title("Executive Overview")

st.write(
    "Provide management with an overall picture of loan applicants and credit risk."
)


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

contract_type = st.sidebar.multiselect(
    "Contract Type",
    df["NAME_CONTRACT_TYPE"].dropna().unique(),
    default=df["NAME_CONTRACT_TYPE"].dropna().unique()
)

education = st.sidebar.multiselect(
    "Education",
    df["NAME_EDUCATION_TYPE"].dropna().unique(),
    default=df["NAME_EDUCATION_TYPE"].dropna().unique()
)


# ---------------- APPLY FILTERS ----------------

df_filtered = df[
    (df["CODE_GENDER"].isin(gender)) &
    (df["NAME_INCOME_TYPE"].isin(income_type)) &
    (df["NAME_CONTRACT_TYPE"].isin(contract_type)) &
    (df["NAME_EDUCATION_TYPE"].isin(education))
]


# ---------------- KPI CALCULATIONS ----------------

total_applications = len(df_filtered)

total_default = (
    df_filtered["TARGET"] == 1
).sum()

total_non_default = (
    df_filtered["TARGET"] == 0
).sum()

default_rate = (
    total_default / total_applications * 100
    if total_applications != 0
    else 0
)

total_credit = (
    df_filtered["AMT_CREDIT"].sum()
)

average_credit = (
    df_filtered["AMT_CREDIT"].mean()
)

average_income = (
    df_filtered["AMT_INCOME_TOTAL"].mean()
)

average_annuity = (
    df_filtered["AMT_ANNUITY"].mean()
)


# ---------------- KPI CARDS ----------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Applications",
    f"{total_applications:,}"
)

col2.metric(
    "Total Default Customers",
    f"{total_default:,}"
)

col3.metric(
    "Total Non-Default Customers",
    f"{total_non_default:,}"
)

col4.metric(
    "Default Rate %",
    f"{default_rate:.2f}%"
)


col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Total Credit Amount",
    f"{total_credit:,.0f}"
)

col6.metric(
    "Average Credit Amount",
    f"{average_credit:,.0f}"
)

col7.metric(
    "Average Income",
    f"{average_income:,.0f}"
)

col8.metric(
    "Average Annuity",
    f"{average_annuity:,.0f}"
)


# ---------------- DEFAULT VS NON-DEFAULT ----------------

st.subheader("Default vs Non-Default Customers")

default_data = (
    df_filtered["TARGET"]
    .value_counts()
    .reset_index()
)

default_data.columns = [
    "Target",
    "Customers"
]

default_data["Status"] = default_data["Target"].map({
    0: "Non-Default",
    1: "Default"
})

st.bar_chart(
    default_data,
    x="Status",
    y="Customers"
)


# ---------------- APPLICATIONS BY GENDER ----------------

st.subheader("Total Applications by Gender")

applications_by_gender = (
    df_filtered
    .groupby("CODE_GENDER")
    .size()
    .reset_index(name="Applications")
)

applications_by_gender.columns = [
    "Gender",
    "Applications"
]

st.bar_chart(
    applications_by_gender,
    x="Gender",
    y="Applications"
)


# ---------------- APPLICATIONS BY CONTRACT TYPE ----------------

st.subheader("Applications by Contract Type")

applications_by_contract = (
    df_filtered
    .groupby("NAME_CONTRACT_TYPE")
    .size()
    .reset_index(name="Applications")
)

applications_by_contract.columns = [
    "Contract Type",
    "Applications"
]

st.bar_chart(
    applications_by_contract,
    x="Contract Type",
    y="Applications"
)


# ---------------- APPLICATIONS BY INCOME TYPE ----------------

st.subheader("Applications by Income Type")

applications_by_income = (
    df_filtered
    .groupby("NAME_INCOME_TYPE")
    .size()
    .reset_index(name="Applications")
)

applications_by_income.columns = [
    "Income Type",
    "Applications"
]

st.bar_chart(
    applications_by_income,
    x="Income Type",
    y="Applications"
)


# ---------------- CREDIT AMOUNT DISTRIBUTION ----------------

st.subheader("Credit Amount Distribution")

st.plotly_chart(
    px.histogram(
        df_filtered,
        x="AMT_CREDIT",
        nbins=40,
        title="Credit Amount Distribution"
    ),
    use_container_width=True
)


# ---------------- OVERALL APPLICANT SUMMARY ----------------

st.subheader("Overall Applicant Summary")

overall_summary = pd.DataFrame({
    "Metric": [
        "Total Applications",
        "Total Default Customers",
        "Total Non-Default Customers",
        "Default Rate %",
        "Average Credit Amount",
        "Average Income",
        "Average Annuity"
    ],
    "Value": [
        total_applications,
        total_default,
        total_non_default,
        round(default_rate, 2),
        round(average_credit, 2),
        round(average_income, 2),
        round(average_annuity, 2)
    ]
})

st.dataframe(
    overall_summary,
    use_container_width=True,
    hide_index=True
)


# ---------------- ADDITIONAL INFORMATION ----------------

st.subheader("Important Insights")


# Most common income type

most_common_income = (
    df_filtered["NAME_INCOME_TYPE"]
    .mode()[0]
)


# Most common education level

most_common_education = (
    df_filtered["NAME_EDUCATION_TYPE"]
    .mode()[0]
)


# Highest risk gender

risk_by_gender = (
    df_filtered
    .groupby("CODE_GENDER")["TARGET"]
    .mean()
)

highest_risk_gender = (
    risk_by_gender.idxmax()
)

highest_risk_gender_rate = (
    risk_by_gender.max() * 100
)


# Highest risk income type

risk_by_income = (
    df_filtered
    .groupby("NAME_INCOME_TYPE")["TARGET"]
    .mean()
)

highest_risk_income = (
    risk_by_income.idxmax()
)

highest_risk_income_rate = (
    risk_by_income.max() * 100
)


# Highest risk customer segment

risk_by_segment = (
    df_filtered
    .groupby(
        [
            "CODE_GENDER",
            "NAME_INCOME_TYPE"
        ]
    )["TARGET"]
    .mean()
    .reset_index()
)

risk_by_segment["Default Rate"] = (
    risk_by_segment["TARGET"] * 100
)

highest_risk_segment = (
    risk_by_segment
    .loc[
        risk_by_segment["Default Rate"].idxmax()
    ]
)


# ---------------- DISPLAY INSIGHTS ----------------

st.write(
    "Overall Default Rate:",
    f"{default_rate:.2f}%"
)

st.write(
    "Average Customer Income:",
    f"{average_income:,.0f}"
)

st.write(
    "Average Loan Amount:",
    f"{average_credit:,.0f}"
)

st.write(
    "Most Common Income Type:",
    most_common_income
)

st.write(
    "Most Common Education Level:",
    most_common_education
)

st.write(
    "Highest Risk Gender:",
    f"{highest_risk_gender} "
    f"({highest_risk_gender_rate:.2f}% default rate)"
)

st.write(
    "Highest Risk Income Type:",
    f"{highest_risk_income} "
    f"({highest_risk_income_rate:.2f}% default rate)"
)

st.write(
    "Highest Risk Customer Segment:",
    f"Gender = {highest_risk_segment['CODE_GENDER']}, "
    f"Income Type = {highest_risk_segment['NAME_INCOME_TYPE']} "
    f"({highest_risk_segment['Default Rate']:.2f}% default rate)"
)
