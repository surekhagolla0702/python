import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Annuity Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("Annuity Analysis")

st.write(
    "Study customers' annual loan payment obligations."
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

average_annuity = df["AMT_ANNUITY"].mean()

median_annuity = df["AMT_ANNUITY"].median()

maximum_annuity = df["AMT_ANNUITY"].max()

average_annuity_defaulters = (
    df.loc[
        df["TARGET"] == 1,
        "AMT_ANNUITY"
    ].mean()
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Annuity",
    f"{average_annuity:,.0f}"
)

col2.metric(
    "Median Annuity",
    f"{median_annuity:,.0f}"
)

col3.metric(
    "Maximum Annuity",
    f"{maximum_annuity:,.0f}"
)

col4.metric(
    "Avg Annuity for Defaulters",
    f"{average_annuity_defaulters:,.0f}"
)


# ---------------------------------------------------------
# ANNUITY DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Annuity Distribution")

fig_distribution = px.histogram(
    df,
    x="AMT_ANNUITY",
    nbins=40,
    title="Annuity Distribution"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ---------------------------------------------------------
# ANNUITY BY TARGET
# ---------------------------------------------------------

st.subheader("Annuity by TARGET")

target_annuity = (
    df.groupby("TARGET")["AMT_ANNUITY"]
    .mean()
    .reset_index()
)

target_annuity["TARGET"] = (
    target_annuity["TARGET"]
    .map({
        0: "Non-Default",
        1: "Default"
    })
)

fig_target = px.bar(
    target_annuity,
    x="TARGET",
    y="AMT_ANNUITY",
    title="Average Annuity by TARGET",
    text="AMT_ANNUITY"
)

st.plotly_chart(
    fig_target,
    use_container_width=True
)


# ---------------------------------------------------------
# ANNUITY VS INCOME
# ---------------------------------------------------------

st.subheader("Annuity vs Income")

fig_income = px.scatter(
    df,
    x="AMT_INCOME_TOTAL",
    y="AMT_ANNUITY",
    color="TARGET",
    title="Annuity vs Income",
    labels={
        "AMT_INCOME_TOTAL": "Income",
        "AMT_ANNUITY": "Annuity",
        "TARGET": "Default"
    }
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ---------------------------------------------------------
# ANNUITY VS CREDIT
# ---------------------------------------------------------

st.subheader("Annuity vs Credit")

fig_credit = px.scatter(
    df,
    x="AMT_CREDIT",
    y="AMT_ANNUITY",
    color="TARGET",
    title="Annuity vs Credit",
    labels={
        "AMT_CREDIT": "Credit Amount",
        "AMT_ANNUITY": "Annuity",
        "TARGET": "Default"
    }
)

st.plotly_chart(
    fig_credit,
    use_container_width=True
)


# ---------------------------------------------------------
# AVERAGE ANNUITY BY INCOME TYPE
# ---------------------------------------------------------

st.subheader("Average Annuity by Income Type")

income_annuity = (
    df.groupby("NAME_INCOME_TYPE")["AMT_ANNUITY"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

income_annuity.columns = [
    "Income Type",
    "Average Annuity"
]

fig_income_type = px.bar(
    income_annuity,
    x="Income Type",
    y="Average Annuity",
    title="Average Annuity by Income Type",
    text="Average Annuity"
)

st.plotly_chart(
    fig_income_type,
    use_container_width=True
)


# ---------------------------------------------------------
# ANNUITY GROUPS
# ---------------------------------------------------------

annuity_bins = [
    0,
    10000,
    20000,
    30000,
    50000,
    75000,
    100000,
    float("inf")
]

annuity_labels = [
    "Below 10K",
    "10K–20K",
    "20K–30K",
    "30K–50K",
    "50K–75K",
    "75K–100K",
    "Above 100K"
]

df["ANNUITY_GROUP"] = pd.cut(
    df["AMT_ANNUITY"],
    bins=annuity_bins,
    labels=annuity_labels,
    include_lowest=True,
    right=False
)


# ---------------------------------------------------------
# DEFAULT RATE BY ANNUITY GROUP
# ---------------------------------------------------------

st.subheader("Default Rate by Annuity Group")

annuity_default = (
    df.groupby(
        "ANNUITY_GROUP",
        observed=False
    )["TARGET"]
    .mean()
    .reindex(annuity_labels)
    .reset_index()
)

annuity_default["Default Rate (%)"] = (
    annuity_default["TARGET"] * 100
)

fig_default = px.bar(
    annuity_default,
    x="ANNUITY_GROUP",
    y="Default Rate (%)",
    title="Default Rate by Annuity Group",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)
