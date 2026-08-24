import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Annuity Burden Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("Annuity Burden Analysis")

st.write(
    "Understand the repayment burden relative to customer income."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)
df = create_features(df)


# ---------------------------------------------------------
# ANNUITY-INCOME RATIO
# ---------------------------------------------------------

df["ANNUITY_INCOME_RATIO"] = (
    df["AMT_ANNUITY"] /
    df["AMT_INCOME_TOTAL"]
)

df["ANNUITY_INCOME_RATIO"] = (
    df["ANNUITY_INCOME_RATIO"]
    .replace(
        [float("inf"), -float("inf")],
        pd.NA
    )
)


# ---------------------------------------------------------
# RISK GROUPS
# ---------------------------------------------------------

def assign_burden_group(ratio):

    if ratio < 0.20:
        return "Low Repayment Burden"

    elif ratio < 0.40:
        return "Medium Repayment Burden"

    elif ratio < 0.60:
        return "High Repayment Burden"

    else:
        return "Very High Repayment Burden"


df["BURDEN_GROUP"] = (
    df["ANNUITY_INCOME_RATIO"]
    .apply(assign_burden_group)
)


# ---------------------------------------------------------
# ANNUITY-TO-INCOME DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Annuity-to-Income Distribution")

fig_distribution = px.histogram(
    df,
    x="ANNUITY_INCOME_RATIO",
    nbins=50,
    title="Annuity-to-Income Ratio Distribution",
    labels={
        "ANNUITY_INCOME_RATIO":
        "Annuity / Income Ratio"
    }
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY RATIO
# ---------------------------------------------------------

st.subheader("Default Rate by Ratio")

ratio_bins = [
    0,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.80,
    1.00,
    float("inf")
]

ratio_labels = [
    "<10%",
    "10–20%",
    "20–30%",
    "30–40%",
    "40–50%",
    "50–60%",
    "60–80%",
    "80–100%",
    "100%+"
]

df["BURDEN_RATIO_RANGE"] = pd.cut(
    df["ANNUITY_INCOME_RATIO"],
    bins=ratio_bins,
    labels=ratio_labels,
    include_lowest=True,
    right=False
)

ratio_default = (
    df.groupby(
        "BURDEN_RATIO_RANGE",
        observed=False
    )["TARGET"]
    .mean()
    .reindex(ratio_labels)
    .reset_index()
)

ratio_default["Default Rate (%)"] = (
    ratio_default["TARGET"] * 100
)

fig_default = px.bar(
    ratio_default,
    x="BURDEN_RATIO_RANGE",
    y="Default Rate (%)",
    title="Default Rate by Annuity-to-Income Ratio",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)


# ---------------------------------------------------------
# RATIO BY GENDER
# ---------------------------------------------------------

st.subheader("Ratio by Gender")

gender_ratio = (
    df.groupby("CODE_GENDER")[
        "ANNUITY_INCOME_RATIO"
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
    y="ANNUITY_INCOME_RATIO",
    title="Average Annuity-to-Income Ratio by Gender",
    text="ANNUITY_INCOME_RATIO"
)

st.plotly_chart(
    fig_gender,
    use_container_width=True
)


# ---------------------------------------------------------
# RATIO BY INCOME TYPE
# ---------------------------------------------------------

st.subheader("Ratio by Income Type")

income_ratio = (
    df.groupby("NAME_INCOME_TYPE")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

income_ratio.columns = [
    "Income Type",
    "Average Annuity-to-Income Ratio"
]

fig_income = px.bar(
    income_ratio,
    x="Income Type",
    y="Average Annuity-to-Income Ratio",
    title="Annuity-to-Income Ratio by Income Type",
    text="Average Annuity-to-Income Ratio"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ---------------------------------------------------------
# RATIO BY EDUCATION
# ---------------------------------------------------------

st.subheader("Ratio by Education")

education_ratio = (
    df.groupby("NAME_EDUCATION_TYPE")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

education_ratio.columns = [
    "Education",
    "Average Annuity-to-Income Ratio"
]

fig_education = px.bar(
    education_ratio,
    x="Education",
    y="Average Annuity-to-Income Ratio",
    title="Annuity-to-Income Ratio by Education",
    text="Average Annuity-to-Income Ratio"
)

st.plotly_chart(
    fig_education,
    use_container_width=True
)


# ---------------------------------------------------------
# RATIO VS TARGET
# ---------------------------------------------------------

st.subheader("Ratio vs TARGET")

target_ratio = (
    df.groupby("TARGET")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
    .reset_index()
)

target_ratio["TARGET"] = (
    target_ratio["TARGET"]
    .map({
        0: "Non-Default",
        1: "Default"
    })
)

fig_target = px.bar(
    target_ratio,
    x="TARGET",
    y="ANNUITY_INCOME_RATIO",
    title="Average Annuity-to-Income Ratio vs TARGET",
    text="ANNUITY_INCOME_RATIO"
)

st.plotly_chart(
    fig_target,
    use_container_width=True
)


# ---------------------------------------------------------
# RISK GROUP SUMMARY
# ---------------------------------------------------------

st.subheader("Repayment Burden Risk Groups")

risk_order = [
    "Low Repayment Burden",
    "Medium Repayment Burden",
    "High Repayment Burden",
    "Very High Repayment Burden"
]

risk_summary = (
    df.groupby(
        "BURDEN_GROUP",
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
            "BURDEN_GROUP",
            "Customers",
            "Defaults",
            "Default Rate (%)"
        ]
    ],
    use_container_width=True
)
