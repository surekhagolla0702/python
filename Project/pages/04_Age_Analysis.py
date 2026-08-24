import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Age Analysis",
    page_icon="📅",
    layout="wide"
)

st.title("Age Analysis")

st.write(
    "Analyze the relationship between age and credit risk."
)


# ---------------- LOAD DATASET ----------------

df = pd.read_csv("data/application_train.csv")


# ---------------- AGE CALCULATION ----------------

df["AGE_YEARS"] = (
    abs(df["DAYS_BIRTH"]) / 365
)


# ---------------- SIDEBAR FILTER ----------------

st.sidebar.header("Filters")

min_age = int(df["AGE_YEARS"].min())
max_age = int(df["AGE_YEARS"].max())

age_range = st.sidebar.slider(
    "Age Range",
    min_age,
    max_age,
    (min_age, max_age)
)


# ---------------- APPLY FILTER ----------------

df_filtered = df[
    df["AGE_YEARS"].between(
        age_range[0],
        age_range[1]
    )
].copy()


# ---------------- AGE GROUPS ----------------

age_bins = [
    18,
    25,
    30,
    35,
    40,
    45,
    50,
    55,
    60,
    150
]

age_labels = [
    "18–25",
    "26–30",
    "31–35",
    "36–40",
    "41–45",
    "46–50",
    "51–55",
    "56–60",
    "61+"
]

df_filtered["AGE_GROUP"] = pd.cut(
    df_filtered["AGE_YEARS"],
    bins=age_bins,
    labels=age_labels,
    include_lowest=True
)


# ---------------- CHECK DATA ----------------

if df_filtered.empty:
    st.warning("No customers available for the selected age range.")
    st.stop()


# ---------------- KPI CALCULATIONS ----------------

average_age = (
    df_filtered["AGE_YEARS"].mean()
)

youngest_customer = (
    df_filtered["AGE_YEARS"].min()
)

oldest_customer = (
    df_filtered["AGE_YEARS"].max()
)

risk_by_age_group = (
    df_filtered
    .groupby("AGE_GROUP", observed=False)["TARGET"]
    .mean()
)

highest_risk_age_group = (
    risk_by_age_group.idxmax()
)


# ---------------- KPI CARDS ----------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Age",
    f"{average_age:.1f} years"
)

col2.metric(
    "Youngest Customer",
    f"{youngest_customer:.1f} years"
)

col3.metric(
    "Oldest Customer",
    f"{oldest_customer:.1f} years"
)

col4.metric(
    "Highest Risk Age Group",
    str(highest_risk_age_group)
)


# ---------------- AGE DISTRIBUTION ----------------

st.subheader("Age Distribution Histogram")

fig_age = px.histogram(
    df_filtered,
    x="AGE_YEARS",
    nbins=30,
    title="Age Distribution"
)

st.plotly_chart(
    fig_age,
    use_container_width=True
)


# ---------------- APPLICATIONS BY AGE GROUP ----------------

st.subheader("Applications by Age Group")

applications_age = (
    df_filtered["AGE_GROUP"]
    .value_counts()
    .reindex(age_labels)
    .reset_index()
)

applications_age.columns = [
    "Age Group",
    "Applications"
]

st.bar_chart(
    applications_age,
    x="Age Group",
    y="Applications"
)


# ---------------- DEFAULT RATE BY AGE ----------------

st.subheader("Default Rate by Age")

default_age = (
    df_filtered
    .groupby("AGE_YEARS")["TARGET"]
    .mean()
    .reset_index()
)

default_age["Default Rate (%)"] = (
    default_age["TARGET"] * 100
)

st.line_chart(
    default_age.set_index("AGE_YEARS")[
        "Default Rate (%)"
    ]
)


# ---------------- DEFAULT RATE BY AGE GROUP ----------------

st.subheader("Default Rate by Age Group")

default_age_group = (
    df_filtered
    .groupby("AGE_GROUP", observed=False)["TARGET"]
    .mean()
    .reindex(age_labels)
    .reset_index()
)

default_age_group["Default Rate (%)"] = (
    default_age_group["TARGET"] * 100
)

default_age_group.columns = [
    "Age Group",
    "Target",
    "Default Rate (%)"
]

st.bar_chart(
    default_age_group,
    x="Age Group",
    y="Default Rate (%)"
)


# ---------------- CREDIT AMOUNT BY AGE ----------------

st.subheader("Credit Amount by Age")

credit_age = (
    df_filtered
    .groupby("AGE_YEARS")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

credit_age.columns = [
    "Age",
    "Average Credit"
]

st.line_chart(
    credit_age.set_index("Age")
)


# ---------------- INCOME BY AGE ----------------

st.subheader("Income by Age")

income_age = (
    df_filtered
    .groupby("AGE_YEARS")["AMT_INCOME_TOTAL"]
    .mean()
    .reset_index()
)

income_age.columns = [
    "Age",
    "Average Income"
]

st.line_chart(
    income_age.set_index("Age")
)


# ---------------- ADDITIONAL INFORMATION ----------------

st.subheader("Additional Information")

highest_risk_rate = (
    risk_by_age_group.max() * 100
)

st.write(
    "Average Age:",
    f"{average_age:.1f} years"
)

st.write(
    "Youngest Customer:",
    f"{youngest_customer:.1f} years"
)

st.write(
    "Oldest Customer:",
    f"{oldest_customer:.1f} years"
)

st.write(
    "Highest Risk Age Group:",
    f"{highest_risk_age_group} "
    f"({highest_risk_rate:.2f}% default rate)"
)
