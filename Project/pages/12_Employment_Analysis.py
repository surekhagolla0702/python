import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Employment Analysis",
    page_icon="💼",
    layout="wide"
)

st.title("Employment Analysis")

st.write(
    "Understand how employment status and work history affect credit risk."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)
df = create_features(df)


# ---------------------------------------------------------
# CLEAN DAYS_EMPLOYED
# ---------------------------------------------------------

# Home Credit uses 365243 as a special value
# for unemployed / missing employment information.

df["DAYS_EMPLOYED_CLEAN"] = df["DAYS_EMPLOYED"].replace(
    365243,
    pd.NA
)


# ---------------------------------------------------------
# EMPLOYMENT YEARS
# ---------------------------------------------------------

df["EMPLOYMENT_YEARS"] = (
    df["DAYS_EMPLOYED_CLEAN"].abs() / 365
)


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

average_employment_years = (
    df["EMPLOYMENT_YEARS"].mean()
)


most_common_occupation = (
    df["OCCUPATION_TYPE"]
    .dropna()
    .mode()
)

if len(most_common_occupation) > 0:
    most_common_occupation = most_common_occupation.iloc[0]
else:
    most_common_occupation = "N/A"


most_common_income_type = (
    df["NAME_INCOME_TYPE"]
    .dropna()
    .mode()
)

if len(most_common_income_type) > 0:
    most_common_income_type = most_common_income_type.iloc[0]
else:
    most_common_income_type = "N/A"


# Highest risk occupation

occupation_risk = (
    df.dropna(subset=["OCCUPATION_TYPE"])
    .groupby("OCCUPATION_TYPE")["TARGET"]
    .mean()
    .sort_values(ascending=False)
)

if len(occupation_risk) > 0:
    highest_risk_occupation = occupation_risk.index[0]
else:
    highest_risk_occupation = "N/A"


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Employment Years",
    f"{average_employment_years:.2f}"
)

col2.metric(
    "Most Common Occupation",
    most_common_occupation
)

col3.metric(
    "Most Common Income Type",
    most_common_income_type
)

col4.metric(
    "Highest Risk Occupation",
    highest_risk_occupation
)


# ---------------------------------------------------------
# EMPLOYMENT YEARS DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Employment Years Distribution")

fig_employment = px.histogram(
    df.dropna(subset=["EMPLOYMENT_YEARS"]),
    x="EMPLOYMENT_YEARS",
    nbins=40,
    title="Employment Years Distribution",
    labels={
        "EMPLOYMENT_YEARS": "Employment Years"
    }
)

st.plotly_chart(
    fig_employment,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY EMPLOYMENT YEARS
# ---------------------------------------------------------

st.subheader("Default Rate by Employment Years")

employment_bins = [
    0,
    1,
    3,
    5,
    10,
    15,
    20,
    30,
    float("inf")
]

employment_labels = [
    "0–1 Years",
    "1–3 Years",
    "3–5 Years",
    "5–10 Years",
    "10–15 Years",
    "15–20 Years",
    "20–30 Years",
    "30+ Years"
]

df["EMPLOYMENT_GROUP"] = pd.cut(
    df["EMPLOYMENT_YEARS"],
    bins=employment_bins,
    labels=employment_labels,
    include_lowest=True,
    right=False
)

employment_default = (
    df.groupby(
        "EMPLOYMENT_GROUP",
        observed=False
    )["TARGET"]
    .mean()
    .reindex(employment_labels)
    .reset_index()
)

employment_default["Default Rate (%)"] = (
    employment_default["TARGET"] * 100
)

fig_employment_default = px.bar(
    employment_default,
    x="EMPLOYMENT_GROUP",
    y="Default Rate (%)",
    title="Default Rate by Employment Years",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_employment_default,
    use_container_width=True
)


# ---------------------------------------------------------
# APPLICATIONS BY INCOME TYPE
# ---------------------------------------------------------

st.subheader("Applications by Income Type")

income_count = (
    df["NAME_INCOME_TYPE"]
    .value_counts()
    .reset_index()
)

income_count.columns = [
    "Income Type",
    "Applications"
]

fig_income_count = px.bar(
    income_count,
    x="Income Type",
    y="Applications",
    title="Applications by Income Type",
    text="Applications"
)

st.plotly_chart(
    fig_income_count,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY INCOME TYPE
# ---------------------------------------------------------

st.subheader("Default Rate by Income Type")

income_default = (
    df.dropna(subset=["NAME_INCOME_TYPE"])
    .groupby("NAME_INCOME_TYPE")["TARGET"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

income_default["Default Rate (%)"] = (
    income_default["TARGET"] * 100
)

fig_income_default = px.bar(
    income_default,
    x="NAME_INCOME_TYPE",
    y="Default Rate (%)",
    title="Default Rate by Income Type",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_income_default,
    use_container_width=True
)


# ---------------------------------------------------------
# APPLICATIONS BY OCCUPATION
# ---------------------------------------------------------

st.subheader("Applications by Occupation")

occupation_count = (
    df["OCCUPATION_TYPE"]
    .dropna()
    .value_counts()
    .reset_index()
)

occupation_count.columns = [
    "Occupation",
    "Applications"
]

fig_occupation_count = px.bar(
    occupation_count,
    x="Occupation",
    y="Applications",
    title="Applications by Occupation",
    text="Applications"
)

st.plotly_chart(
    fig_occupation_count,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY OCCUPATION
# ---------------------------------------------------------

st.subheader("Default Rate by Occupation")

occupation_default = (
    df.dropna(subset=["OCCUPATION_TYPE"])
    .groupby("OCCUPATION_TYPE")["TARGET"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

occupation_default["Default Rate (%)"] = (
    occupation_default["TARGET"] * 100
)

fig_occupation_default = px.bar(
    occupation_default,
    x="OCCUPATION_TYPE",
    y="Default Rate (%)",
    title="Default Rate by Occupation",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_occupation_default,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY ORGANIZATION TYPE
# ---------------------------------------------------------

st.subheader("Default Rate by Organization Type")

organization_default = (
    df.dropna(subset=["ORGANIZATION_TYPE"])
    .groupby("ORGANIZATION_TYPE")["TARGET"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

organization_default["Default Rate (%)"] = (
    organization_default["TARGET"] * 100
)

fig_organization = px.bar(
    organization_default,
    x="ORGANIZATION_TYPE",
    y="Default Rate (%)",
    title="Default Rate by Organization Type",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_organization,
    use_container_width=True
)
