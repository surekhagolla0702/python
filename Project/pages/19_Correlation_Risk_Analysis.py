import streamlit as st
import pandas as pd
import plotly.express as px


from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Correlation & Risk Factor Analysis",
    page_icon="📈",
    layout="wide"
)

st.title(
    "Correlation & Risk Factor Analysis"
)

st.write(
    "Identify important numerical relationships "
    "associated with loan default."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)
df = create_features(df)


# ---------------------------------------------------------
# DERIVED FEATURES
# ---------------------------------------------------------

df["AGE_YEARS"] = (
    df["DAYS_BIRTH"].abs() / 365
)

df["EMPLOYMENT_YEARS"] = (
    df["DAYS_EMPLOYED"].abs() / 365
)

df["CREDIT_INCOME_RATIO"] = (
    df["AMT_CREDIT"] /
    df["AMT_INCOME_TOTAL"]
)

df["ANNUITY_INCOME_RATIO"] = (
    df["AMT_ANNUITY"] /
    df["AMT_INCOME_TOTAL"]
)

df["CREDIT_GOODS_RATIO"] = (
    df["AMT_CREDIT"] /
    df["AMT_GOODS_PRICE"]
)

df["AVERAGE_EXTERNAL_SCORE"] = (
    df[
        [
            "EXT_SOURCE_1",
            "EXT_SOURCE_2",
            "EXT_SOURCE_3"
        ]
    ].mean(axis=1)
)

df = df.replace(
    [float("inf"), -float("inf")],
    pd.NA
)


# ---------------------------------------------------------
# NUMERICAL FEATURES
# ---------------------------------------------------------

numerical_features = [
    "TARGET",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",
    "CNT_CHILDREN",
    "CNT_FAM_MEMBERS"
]

numerical_features = [
    column
    for column in numerical_features
    if column in df.columns
]


# ---------------------------------------------------------
# CORRELATION MATRIX
# ---------------------------------------------------------

correlation_matrix = (
    df[numerical_features]
    .corr()
)


# ---------------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------------

st.subheader("Correlation Heatmap")

fig_heatmap = px.imshow(
    correlation_matrix,
    text_auto=".2f",
    aspect="auto",
    title="Correlation Heatmap",
    color_continuous_scale="RdBu_r"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)


# ---------------------------------------------------------
# CORRELATION WITH TARGET
# ---------------------------------------------------------

st.subheader("Correlation with TARGET")

target_correlation = (
    correlation_matrix["TARGET"]
    .drop("TARGET")
    .sort_values()
    .reset_index()
)

target_correlation.columns = [
    "Feature",
    "Correlation"
]

fig_target_corr = px.bar(
    target_correlation,
    x="Correlation",
    y="Feature",
    orientation="h",
    title="Correlation with TARGET",
    text="Correlation"
)

st.plotly_chart(
    fig_target_corr,
    use_container_width=True
)


# ---------------------------------------------------------
# TOP POSITIVE CORRELATIONS
# ---------------------------------------------------------

st.subheader("Top Positive Correlations")

positive_corr = (
    target_correlation[
        target_correlation["Correlation"] > 0
    ]
    .sort_values(
        "Correlation",
        ascending=False
    )
    .head(10)
)

if not positive_corr.empty:

    fig_positive = px.bar(
        positive_corr,
        x="Correlation",
        y="Feature",
        orientation="h",
        title="Top Positive Correlations with TARGET",
        text="Correlation"
    )

    st.plotly_chart(
        fig_positive,
        use_container_width=True
    )

else:

    st.info(
        "No positive correlations found."
    )


# ---------------------------------------------------------
# TOP NEGATIVE CORRELATIONS
# ---------------------------------------------------------

st.subheader("Top Negative Correlations")

negative_corr = (
    target_correlation[
        target_correlation["Correlation"] < 0
    ]
    .sort_values(
        "Correlation",
        ascending=True
    )
    .head(10)
)

if not negative_corr.empty:

    fig_negative = px.bar(
        negative_corr,
        x="Correlation",
        y="Feature",
        orientation="h",
        title="Top Negative Correlations with TARGET",
        text="Correlation"
    )

    st.plotly_chart(
        fig_negative,
        use_container_width=True
    )

else:

    st.info(
        "No negative correlations found."
    )


# ---------------------------------------------------------
# CREDIT VS INCOME
# ---------------------------------------------------------

st.subheader("Credit vs Income Scatter Plot")

fig_credit_income = px.scatter(
    df,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    color="TARGET",
    opacity=0.5,
    title="Credit vs Income",
    labels={
        "AMT_INCOME_TOTAL": "Income",
        "AMT_CREDIT": "Credit Amount",
        "TARGET": "Default"
    }
)

st.plotly_chart(
    fig_credit_income,
    use_container_width=True
)


# ---------------------------------------------------------
# EXTERNAL SCORE VS TARGET
# ---------------------------------------------------------

st.subheader("External Score vs TARGET")

external_columns = [
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3"
]

external_available = [
    column
    for column in external_columns
    if column in df.columns
]

external_target = (
    df.groupby("TARGET")[external_available]
    .mean()
    .reset_index()
)

external_target["TARGET"] = (
    external_target["TARGET"]
    .map({
        0: "Non-Default",
        1: "Default"
    })
)

external_target = external_target.melt(
    id_vars="TARGET",
    var_name="External Score",
    value_name="Average Score"
)

fig_external_target = px.bar(
    external_target,
    x="External Score",
    y="Average Score",
    color="TARGET",
    barmode="group",
    title="External Score vs TARGET"
)

st.plotly_chart(
    fig_external_target,
    use_container_width=True
)


# ---------------------------------------------------------
# AGE GROUP
# ---------------------------------------------------------

df["AGE_GROUP"] = pd.cut(
    df["AGE_YEARS"],
    bins=[
        0,
        25,
        35,
        45,
        55,
        100
    ],
    labels=[
        "Below 25",
        "25-35",
        "35-45",
        "45-55",
        "55+"
    ]
)


# ---------------------------------------------------------
# AGE GROUP VS DEFAULT
# ---------------------------------------------------------

st.subheader("Age Group vs Default")

age_default = (
    df.groupby(
        "AGE_GROUP",
        observed=False
    )["TARGET"]
    .mean()
    .reset_index()
)

age_default["Default Rate (%)"] = (
    age_default["TARGET"] * 100
)

fig_age_default = px.bar(
    age_default,
    x="AGE_GROUP",
    y="Default Rate (%)",
    title="Default Rate by Age Group",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_age_default,
    use_container_width=True
)


# ---------------------------------------------------------
# EMPLOYMENT HISTORY VS DEFAULT
# ---------------------------------------------------------

st.subheader(
    "Employment History vs Default"
)

employment_group = pd.cut(
    df["EMPLOYMENT_YEARS"],
    bins=[
        0,
        2,
        5,
        10,
        20,
        100
    ],
    labels=[
        "0-2 Years",
        "2-5 Years",
        "5-10 Years",
        "10-20 Years",
        "20+ Years"
    ]
)

employment_default = (
    df.groupby(
        employment_group,
        observed=False
    )["TARGET"]
    .mean()
    .reset_index()
)

employment_default.columns = [
    "Employment Group",
    "Default Rate"
]

employment_default["Default Rate (%)"] = (
    employment_default["Default Rate"] * 100
)

fig_employment_default = px.bar(
    employment_default,
    x="Employment Group",
    y="Default Rate (%)",
    title="Default Rate by Employment History",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_employment_default,
    use_container_width=True
)


# ---------------------------------------------------------
# OCCUPATION VS DEFAULT
# ---------------------------------------------------------

if "OCCUPATION_TYPE" in df.columns:

    st.subheader("Occupation vs Default")

    occupation_default = (
        df.groupby("OCCUPATION_TYPE")["TARGET"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    occupation_default["Default Rate (%)"] = (
        occupation_default["TARGET"] * 100
    )

    fig_occupation = px.bar(
        occupation_default.head(10),
        x="OCCUPATION_TYPE",
        y="Default Rate (%)",
        title="Top 10 Occupations by Default Rate",
        text="Default Rate (%)"
    )

    fig_occupation.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_occupation,
        use_container_width=True
    )


# ---------------------------------------------------------
# INCOME TYPE VS DEFAULT
# ---------------------------------------------------------

if "NAME_INCOME_TYPE" in df.columns:

    st.subheader("Income Type vs Default")

    income_type_default = (
        df.groupby("NAME_INCOME_TYPE")["TARGET"]
        .mean()
        .reset_index()
    )

    income_type_default["Default Rate (%)"] = (
        income_type_default["TARGET"] * 100
    )

    fig_income_type = px.bar(
        income_type_default,
        x="NAME_INCOME_TYPE",
        y="Default Rate (%)",
        title="Default Rate by Income Type",
        text="Default Rate (%)"
    )

    fig_income_type.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_income_type,
        use_container_width=True
    )


# ---------------------------------------------------------
# REGIONAL RISK RATING VS DEFAULT
# ---------------------------------------------------------

if "REGION_RATING_CLIENT" in df.columns:

    st.subheader(
        "Regional Risk Rating vs Default"
    )

    regional_default = (
        df.groupby("REGION_RATING_CLIENT")["TARGET"]
        .mean()
        .reset_index()
    )

    regional_default["Default Rate (%)"] = (
        regional_default["TARGET"] * 100
    )

    fig_regional_default = px.bar(
        regional_default,
        x="REGION_RATING_CLIENT",
        y="Default Rate (%)",
        title="Default Rate by Regional Risk Rating",
        text="Default Rate (%)"
    )

    st.plotly_chart(
        fig_regional_default,
        use_container_width=True
    )


# ---------------------------------------------------------
# IMPORTANT RISK FACTORS
# ---------------------------------------------------------

st.subheader("Important Risk Factors")

st.write(
    "The following factors can be examined as potential "
    "risk indicators based on the analysis:"
)

risk_factors = [
    "Low External Credit Score",
    "High Credit-to-Income Ratio",
    "High Annuity-to-Income Ratio",
    "Certain Occupations",
    "Certain Income Types",
    "Younger Age Groups",
    "Regional Risk Rating",
    "Employment History"
]

for factor in risk_factors:

    st.write(
        f"• {factor}"
    )


# ---------------------------------------------------------
# CREDIT-TO-INCOME RATIO SUMMARY
# ---------------------------------------------------------

st.subheader(
    "Credit-to-Income Ratio Risk Analysis"
)

ratio_summary = (
    df["CREDIT_INCOME_RATIO"]
    .describe()
    .reset_index()
)

ratio_summary.columns = [
    "Statistic",
    "Value"
]

st.dataframe(
    ratio_summary,
    use_container_width=True
)


# ---------------------------------------------------------
# ANNUITY-TO-INCOME RATIO SUMMARY
# ---------------------------------------------------------

st.subheader(
    "Annuity-to-Income Ratio Risk Analysis"
)

annuity_ratio_summary = (
    df["ANNUITY_INCOME_RATIO"]
    .describe()
    .reset_index()
)

annuity_ratio_summary.columns = [
    "Statistic",
    "Value"
]

st.dataframe(
    annuity_ratio_summary,
    use_container_width=True
)


# ---------------------------------------------------------
# CREDIT-TO-GOODS RATIO SUMMARY
# ---------------------------------------------------------

st.subheader(
    "Credit-to-Goods Ratio Risk Analysis"
)

credit_goods_summary = (
    df["CREDIT_GOODS_RATIO"]
    .describe()
    .reset_index()
)

credit_goods_summary.columns = [
    "Statistic",
    "Value"
]

st.dataframe(
    credit_goods_summary,
    use_container_width=True
)

# ---------------------------------------------------------
# TARGET CORRELATION TABLE
# ---------------------------------------------------------

st.subheader("Target Correlation Summary")

target_correlation_display = (
    target_correlation
    .sort_values(
        "Correlation",
        ascending=False
    )
)

st.dataframe(
    target_correlation_display,
    use_container_width=True
)
