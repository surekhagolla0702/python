import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="External Credit Score Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("External Credit Score Analysis")

st.write(
    "Analyze external credit scores and their relationship with TARGET."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)
df = create_features(df)


# ---------------------------------------------------------
# EXTERNAL SCORE COLUMNS
# ---------------------------------------------------------

score_columns = [
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3"
]


# ---------------------------------------------------------
# AVERAGE EXTERNAL SCORE
# ---------------------------------------------------------

df["AVERAGE_EXTERNAL_SCORE"] = (
    df["EXT_SOURCE_1"] +
    df["EXT_SOURCE_2"] +
    df["EXT_SOURCE_3"]
) / 3


# ---------------------------------------------------------
# HIGH / LOW EXTERNAL SCORE
# ---------------------------------------------------------

score_median = (
    df["AVERAGE_EXTERNAL_SCORE"].median()
)

df["EXTERNAL_SCORE_GROUP"] = pd.NA

df.loc[
    df["AVERAGE_EXTERNAL_SCORE"] >= score_median,
    "EXTERNAL_SCORE_GROUP"
] = "High External Score"

df.loc[
    df["AVERAGE_EXTERNAL_SCORE"] < score_median,
    "EXTERNAL_SCORE_GROUP"
] = "Low External Score"


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

average_score_1 = (
    df["EXT_SOURCE_1"].mean()
)

average_score_2 = (
    df["EXT_SOURCE_2"].mean()
)

average_score_3 = (
    df["EXT_SOURCE_3"].mean()
)

missing_external_scores = (
    df[score_columns]
    .isna()
    .any(axis=1)
    .sum()
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average EXT_SOURCE_1",
    f"{average_score_1:.3f}"
)

col2.metric(
    "Average EXT_SOURCE_2",
    f"{average_score_2:.3f}"
)

col3.metric(
    "Average EXT_SOURCE_3",
    f"{average_score_3:.3f}"
)

col4.metric(
    "Missing External Score Records",
    f"{missing_external_scores:,}"
)


# ---------------------------------------------------------
# EXT_SOURCE_1 DISTRIBUTION
# ---------------------------------------------------------

st.subheader("EXT_SOURCE_1 Distribution")

fig_source_1 = px.histogram(
    df,
    x="EXT_SOURCE_1",
    nbins=40,
    title="EXT_SOURCE_1 Distribution"
)

st.plotly_chart(
    fig_source_1,
    use_container_width=True
)


# ---------------------------------------------------------
# EXT_SOURCE_2 DISTRIBUTION
# ---------------------------------------------------------

st.subheader("EXT_SOURCE_2 Distribution")

fig_source_2 = px.histogram(
    df,
    x="EXT_SOURCE_2",
    nbins=40,
    title="EXT_SOURCE_2 Distribution"
)

st.plotly_chart(
    fig_source_2,
    use_container_width=True
)


# ---------------------------------------------------------
# EXT_SOURCE_3 DISTRIBUTION
# ---------------------------------------------------------

st.subheader("EXT_SOURCE_3 Distribution")

fig_source_3 = px.histogram(
    df,
    x="EXT_SOURCE_3",
    nbins=40,
    title="EXT_SOURCE_3 Distribution"
)

st.plotly_chart(
    fig_source_3,
    use_container_width=True
)


# ---------------------------------------------------------
# EXTERNAL SCORES BY TARGET
# ---------------------------------------------------------

st.subheader("External Scores by TARGET")

target_scores = (
    df.groupby("TARGET")[score_columns]
    .mean()
    .reset_index()
)

target_scores["TARGET"] = target_scores["TARGET"].map({
    0: "Non-Default",
    1: "Default"
})

target_scores = target_scores.melt(
    id_vars="TARGET",
    value_vars=score_columns,
    var_name="External Score",
    value_name="Average Score"
)

fig_target = px.bar(
    target_scores,
    x="External Score",
    y="Average Score",
    color="TARGET",
    barmode="group",
    title="External Scores by TARGET"
)

st.plotly_chart(
    fig_target,
    use_container_width=True
)


# ---------------------------------------------------------
# EXT_SOURCE_1 VS EXT_SOURCE_2
# ---------------------------------------------------------

st.subheader("EXT_SOURCE_1 vs EXT_SOURCE_2")

fig_source_12 = px.scatter(
    df,
    x="EXT_SOURCE_1",
    y="EXT_SOURCE_2",
    color="TARGET",
    title="EXT_SOURCE_1 vs EXT_SOURCE_2",
    labels={
        "TARGET": "Default"
    }
)

st.plotly_chart(
    fig_source_12,
    use_container_width=True
)


# ---------------------------------------------------------
# EXT_SOURCE_2 VS EXT_SOURCE_3
# ---------------------------------------------------------

st.subheader("EXT_SOURCE_2 vs EXT_SOURCE_3")

fig_source_23 = px.scatter(
    df,
    x="EXT_SOURCE_2",
    y="EXT_SOURCE_3",
    color="TARGET",
    title="EXT_SOURCE_2 vs EXT_SOURCE_3",
    labels={
        "TARGET": "Default"
    }
)

st.plotly_chart(
    fig_source_23,
    use_container_width=True
)


# ---------------------------------------------------------
# EXTERNAL SCORE VS DEFAULT RATE
# ---------------------------------------------------------

st.subheader("External Score vs Default Rate")

score_bins = [
    0,
    0.20,
    0.40,
    0.60,
    0.80,
    1.00
]

score_labels = [
    "0–0.20",
    "0.20–0.40",
    "0.40–0.60",
    "0.60–0.80",
    "0.80–1.00"
]

df["AVERAGE_SCORE_GROUP"] = pd.cut(
    df["AVERAGE_EXTERNAL_SCORE"],
    bins=score_bins,
    labels=score_labels,
    include_lowest=True
)

score_default = (
    df.groupby(
        "AVERAGE_SCORE_GROUP",
        observed=False
    )["TARGET"]
    .mean()
    .reindex(score_labels)
    .reset_index()
)

score_default["Default Rate (%)"] = (
    score_default["TARGET"] * 100
)

fig_score_default = px.bar(
    score_default,
    x="AVERAGE_SCORE_GROUP",
    y="Default Rate (%)",
    title="External Score vs Default Rate",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_score_default,
    use_container_width=True
)


# ---------------------------------------------------------
# HIGH VS LOW EXTERNAL SCORE
# ---------------------------------------------------------

st.subheader("High External Score vs Low External Score")

score_group_summary = (
    df.dropna(subset=["EXTERNAL_SCORE_GROUP"])
    .groupby("EXTERNAL_SCORE_GROUP")["TARGET"]
    .agg(
        Customers="count",
        Defaults="sum",
        Default_Rate="mean"
    )
    .reindex([
        "Low External Score",
        "High External Score"
    ])
    .reset_index()
)

score_group_summary["Default Rate (%)"] = (
    score_group_summary["Default_Rate"] * 100
)

st.dataframe(
    score_group_summary[
        [
            "EXTERNAL_SCORE_GROUP",
            "Customers",
            "Defaults",
            "Default Rate (%)"
        ]
    ],
    use_container_width=True
)
