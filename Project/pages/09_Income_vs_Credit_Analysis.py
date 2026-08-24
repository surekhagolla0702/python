import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Income vs Credit Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("Income vs Credit Analysis")

st.write(
    "Determine whether customers are taking loans proportional to their income."
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
# RISK GROUPS
# ---------------------------------------------------------

def assign_risk_group(ratio):

    if ratio < 2:
        return "Low"

    elif ratio < 4:
        return "Moderate"

    elif ratio <= 6:
        return "High"

    else:
        return "Very High"


df["RISK_GROUP"] = (
    df["CREDIT_INCOME_RATIO"]
    .apply(assign_risk_group)
)


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

average_ratio = (
    df["CREDIT_INCOME_RATIO"].mean()
)

highest_ratio = (
    df["CREDIT_INCOME_RATIO"].max()
)

high_ratio_customers = (
    df["CREDIT_INCOME_RATIO"] > 6
)

if high_ratio_customers.sum() > 0:

    high_ratio_default_rate = (
        df.loc[
            high_ratio_customers,
            "TARGET"
        ].mean() * 100
    )

else:

    high_ratio_default_rate = 0


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Credit-to-Income Ratio",
    f"{average_ratio:.2f}"
)

col2.metric(
    "Highest Credit-to-Income Ratio",
    f"{highest_ratio:.2f}"
)

col3.metric(
    "Default Rate for High Ratio Customers",
    f"{high_ratio_default_rate:.2f}%"
)


# ---------------------------------------------------------
# INCOME VS CREDIT SCATTER PLOT
# ---------------------------------------------------------

st.subheader("Income vs Credit Scatter Plot")

fig_scatter = px.scatter(
    df,
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
    fig_scatter,
    use_container_width=True
)


# ---------------------------------------------------------
# CREDIT / INCOME RATIO DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Credit/Income Ratio Distribution")

fig_ratio = px.histogram(
    df,
    x="CREDIT_INCOME_RATIO",
    nbins=50,
    title="Credit-to-Income Ratio Distribution"
)

st.plotly_chart(
    fig_ratio,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE VS CREDIT/INCOME RATIO
# ---------------------------------------------------------

st.subheader("Default Rate vs Credit/Income Ratio")

ratio_bins = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    8,
    10,
    15,
    20,
    float("inf")
]

ratio_labels = [
    "<1",
    "1–2",
    "2–3",
    "3–4",
    "4–5",
    "5–6",
    "6–8",
    "8–10",
    "10–15",
    "15–20",
    "20+"
]

df["RATIO_RANGE"] = pd.cut(
    df["CREDIT_INCOME_RATIO"],
    bins=ratio_bins,
    labels=ratio_labels,
    include_lowest=True,
    right=False
)

ratio_default = (
    df.groupby(
        "RATIO_RANGE",
        observed=False
    )["TARGET"]
    .mean()
    .reindex(ratio_labels)
    .reset_index()
)

ratio_default["Default Rate (%)"] = (
    ratio_default["TARGET"] * 100
)

fig_ratio_default = px.bar(
    ratio_default,
    x="RATIO_RANGE",
    y="Default Rate (%)",
    title="Default Rate vs Credit/Income Ratio",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_ratio_default,
    use_container_width=True
)


# ---------------------------------------------------------
# GENDER-WISE CREDIT / INCOME RATIO
# ---------------------------------------------------------

st.subheader("Gender-wise Credit/Income Ratio")

gender_ratio = (
    df.groupby("CODE_GENDER")[
        "CREDIT_INCOME_RATIO"
    ]
    .mean()
    .reset_index()
)

gender_ratio["Gender"] = (
    gender_ratio["CODE_GENDER"]
    .map({
        "M": "Male",
        "F": "Female"
    })
)

gender_ratio = gender_ratio.dropna(
    subset=["Gender"]
)

fig_gender = px.bar(
    gender_ratio,
    x="Gender",
    y="CREDIT_INCOME_RATIO",
    title="Average Credit/Income Ratio by Gender",
    text="CREDIT_INCOME_RATIO"
)

st.plotly_chart(
    fig_gender,
    use_container_width=True
)


# ---------------------------------------------------------
# EDUCATION-WISE CREDIT / INCOME RATIO
# ---------------------------------------------------------

st.subheader("Education-wise Credit/Income Ratio")

education_ratio = (
    df.groupby("NAME_EDUCATION_TYPE")[
        "CREDIT_INCOME_RATIO"
    ]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

education_ratio.columns = [
    "Education",
    "Average Credit/Income Ratio"
]

fig_education = px.bar(
    education_ratio,
    x="Education",
    y="Average Credit/Income Ratio",
    title="Average Credit/Income Ratio by Education",
    text="Average Credit/Income Ratio"
)

st.plotly_chart(
    fig_education,
    use_container_width=True
)


# ---------------------------------------------------------
# RISK GROUP SUMMARY
# ---------------------------------------------------------

st.subheader("Credit-to-Income Risk Groups")

risk_order = [
    "Low",
    "Moderate",
    "High",
    "Very High"
]

risk_summary = (
    df.groupby(
        "RISK_GROUP",
        observed=False
    )
    .agg(
        Customers=("TARGET", "size"),
        Defaults=("TARGET", "sum"),
        Default_Rate=("TARGET", "mean")
    )
    .reindex(risk_order)
    .reset_index()
)

risk_summary["Default Rate (%)"] = (
    risk_summary["Default_Rate"] * 100
)

st.dataframe(
    risk_summary[
        [
            "RISK_GROUP",
            "Customers",
            "Defaults",
            "Default Rate (%)"
        ]
    ],
    use_container_width=True
)
