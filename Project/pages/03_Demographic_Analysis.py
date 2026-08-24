import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Customer Demographic Analysis",
    page_icon="👥",
    layout="wide"
)

st.title("Customer Demographic Analysis")

st.write(
    "Understand demographic characteristics of Home Credit applicants."
)


# ---------------- LOAD DATASET ----------------

df = pd.read_csv("data/application_train.csv")


# ---------------- CREATE AGE ----------------

df["AGE_YEARS"] = (
    -df["DAYS_BIRTH"] / 365.25
)


# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Demographic Filters")


# Gender

gender = st.sidebar.multiselect(
    "Gender",
    df["CODE_GENDER"].dropna().unique(),
    default=df["CODE_GENDER"].dropna().unique()
)


# Age

min_age = int(df["AGE_YEARS"].min())
max_age = int(df["AGE_YEARS"].max())

age = st.sidebar.slider(
    "Age",
    min_age,
    max_age,
    (min_age, max_age)
)


# Family Status

family_status = st.sidebar.multiselect(
    "Family Status",
    df["NAME_FAMILY_STATUS"].dropna().unique(),
    default=df["NAME_FAMILY_STATUS"].dropna().unique()
)


# Education

education = st.sidebar.multiselect(
    "Education",
    df["NAME_EDUCATION_TYPE"].dropna().unique(),
    default=df["NAME_EDUCATION_TYPE"].dropna().unique()
)


# Housing Type

housing_type = st.sidebar.multiselect(
    "Housing Type",
    df["NAME_HOUSING_TYPE"].dropna().unique(),
    default=df["NAME_HOUSING_TYPE"].dropna().unique()
)


# ---------------- APPLY FILTERS ----------------

df_filtered = df[
    (df["CODE_GENDER"].isin(gender)) &
    (df["AGE_YEARS"].between(age[0], age[1])) &
    (df["NAME_FAMILY_STATUS"].isin(family_status)) &
    (df["NAME_EDUCATION_TYPE"].isin(education)) &
    (df["NAME_HOUSING_TYPE"].isin(housing_type))
]


# ---------------- CHECK FILTERED DATA ----------------

if df_filtered.empty:
    st.warning("No customers available for the selected filters.")
    st.stop()


# ---------------- KPI CALCULATIONS ----------------

total_customers = len(df_filtered)

average_age = (
    df_filtered["AGE_YEARS"].mean()
)

male_customers = (
    df_filtered["CODE_GENDER"] == "M"
).sum()

female_customers = (
    df_filtered["CODE_GENDER"] == "F"
).sum()

average_family_size = (
    df_filtered["CNT_FAM_MEMBERS"].mean()
)


# ---------------- KPI CARDS ----------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Average Age",
    f"{average_age:.1f}"
)

col3.metric(
    "Male Customers",
    f"{male_customers:,}"
)

col4.metric(
    "Female Customers",
    f"{female_customers:,}"
)

col5.metric(
    "Average Family Size",
    f"{average_family_size:.2f}"
)


# ---------------- CUSTOMERS BY GENDER ----------------

st.subheader("Customers by Gender")

customers_by_gender = (
    df_filtered
    .groupby("CODE_GENDER")
    .size()
    .reset_index(name="Customers")
)

customers_by_gender.columns = [
    "Gender",
    "Customers"
]

st.bar_chart(
    customers_by_gender,
    x="Gender",
    y="Customers"
)


# ---------------- CUSTOMERS BY AGE GROUP ----------------

st.subheader("Customers by Age Group")

df_filtered["AGE_GROUP"] = pd.cut(
    df_filtered["AGE_YEARS"],
    bins=[0, 25, 35, 45, 55, 65, 100],
    labels=[
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "56-65",
        "65+"
    ]
)

customers_by_age = (
    df_filtered["AGE_GROUP"]
    .value_counts()
    .sort_index()
    .reset_index()
)

customers_by_age.columns = [
    "Age Group",
    "Customers"
]

st.bar_chart(
    customers_by_age,
    x="Age Group",
    y="Customers"
)


# ---------------- CUSTOMERS BY FAMILY STATUS ----------------

st.subheader("Customers by Family Status")

customers_by_family = (
    df_filtered
    .groupby("NAME_FAMILY_STATUS")
    .size()
    .reset_index(name="Customers")
)

customers_by_family.columns = [
    "Family Status",
    "Customers"
]

st.bar_chart(
    customers_by_family,
    x="Family Status",
    y="Customers"
)


# ---------------- CUSTOMERS BY EDUCATION ----------------

st.subheader("Customers by Education")

customers_by_education = (
    df_filtered
    .groupby("NAME_EDUCATION_TYPE")
    .size()
    .reset_index(name="Customers")
)

customers_by_education.columns = [
    "Education",
    "Customers"
]

st.bar_chart(
    customers_by_education,
    x="Education",
    y="Customers"
)


# ---------------- CUSTOMERS BY HOUSING TYPE ----------------

st.subheader("Customers by Housing Type")

customers_by_housing = (
    df_filtered
    .groupby("NAME_HOUSING_TYPE")
    .size()
    .reset_index(name="Customers")
)

customers_by_housing.columns = [
    "Housing Type",
    "Customers"
]

st.bar_chart(
    customers_by_housing,
    x="Housing Type",
    y="Customers"
)


# ---------------- DEFAULT RATE BY DEMOGRAPHIC GROUP ----------------

st.subheader("Default Rate by Demographic Group")


# Default rate by Gender

default_gender = (
    df_filtered
    .groupby("CODE_GENDER")["TARGET"]
    .mean()
    .reset_index()
)

default_gender["Default Rate (%)"] = (
    default_gender["TARGET"] * 100
)

default_gender.columns = [
    "Gender",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_gender,
    x="Gender",
    y="Default Rate (%)"
)


# Default rate by Age Group

default_age = (
    df_filtered
    .groupby("AGE_GROUP", observed=False)["TARGET"]
    .mean()
    .reset_index()
)

default_age["Default Rate (%)"] = (
    default_age["TARGET"] * 100
)

default_age.columns = [
    "Age Group",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_age,
    x="Age Group",
    y="Default Rate (%)"
)


# Default rate by Family Status

default_family = (
    df_filtered
    .groupby("NAME_FAMILY_STATUS")["TARGET"]
    .mean()
    .reset_index()
)

default_family["Default Rate (%)"] = (
    default_family["TARGET"] * 100
)

default_family.columns = [
    "Family Status",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_family,
    x="Family Status",
    y="Default Rate (%)"
)


# Default rate by Education

default_education = (
    df_filtered
    .groupby("NAME_EDUCATION_TYPE")["TARGET"]
    .mean()
    .reset_index()
)

default_education["Default Rate (%)"] = (
    default_education["TARGET"] * 100
)

default_education.columns = [
    "Education",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_education,
    x="Education",
    y="Default Rate (%)"
)


# Default rate by Housing Type

default_housing = (
    df_filtered
    .groupby("NAME_HOUSING_TYPE")["TARGET"]
    .mean()
    .reset_index()
)

default_housing["Default Rate (%)"] = (
    default_housing["TARGET"] * 100
)

default_housing.columns = [
    "Housing Type",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_housing,
    x="Housing Type",
    y="Default Rate (%)"
)


# ---------------- ADDITIONAL INFORMATION ----------------

st.subheader("Additional Information")


highest_risk_gender = (
    default_gender
    .loc[default_gender["Default Rate (%)"].idxmax()]
)

highest_risk_age = (
    default_age
    .loc[default_age["Default Rate (%)"].idxmax()]
)

highest_risk_family = (
    default_family
    .loc[default_family["Default Rate (%)"].idxmax()]
)

highest_risk_education = (
    default_education
    .loc[default_education["Default Rate (%)"].idxmax()]
)

highest_risk_housing = (
    default_housing
    .loc[default_housing["Default Rate (%)"].idxmax()]
)


st.write(
    "Average Age:",
    f"{average_age:.1f} years"
)

st.write(
    "Average Family Size:",
    f"{average_family_size:.2f}"
)

st.write(
    "Highest Default Rate by Gender:",
    f"{highest_risk_gender['Gender']} "
    f"({highest_risk_gender['Default Rate (%)']:.2f}%)"
)

st.write(
    "Highest Default Rate by Age Group:",
    f"{highest_risk_age['Age Group']} "
    f"({highest_risk_age['Default Rate (%)']:.2f}%)"
)

st.write(
    "Highest Default Rate by Family Status:",
    f"{highest_risk_family['Family Status']} "
    f"({highest_risk_family['Default Rate (%)']:.2f}%)"
)

st.write(
    "Highest Default Rate by Education:",
    f"{highest_risk_education['Education']} "
    f"({highest_risk_education['Default Rate (%)']:.2f}%)"
)

st.write(
    "Highest Default Rate by Housing Type:",
    f"{highest_risk_housing['Housing Type']} "
    f"({highest_risk_housing['Default Rate (%)']:.2f}%)"
)
