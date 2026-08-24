import streamlit as st
import pandas as pd
import plotly.express as px


from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Missing Value Analysis",
    page_icon="🔍",
    layout="wide"
)

st.title("Missing Value Analysis")

st.write(
    "Understand data quality before building machine-learning models."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)
df = create_features(df)


# ---------------------------------------------------------
# MISSING VALUE CALCULATIONS
# ---------------------------------------------------------

missing_count = df.isna().sum()

missing_percentage = (
    df.isna().mean() * 100
)

columns_with_missing = (
    (missing_count > 0).sum()
)

columns_over_50 = (
    (missing_percentage > 50).sum()
)

total_missing_values = (
    missing_count.sum()
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Rows",
    f"{df.shape[0]:,}"
)

col2.metric(
    "Total Columns",
    f"{df.shape[1]:,}"
)

col3.metric(
    "Total Missing Values",
    f"{total_missing_values:,}"
)

col4.metric(
    "Columns with Missing Values",
    f"{columns_with_missing:,}"
)

col5.metric(
    "Columns with >50% Missing Data",
    f"{columns_over_50:,}"
)


# ---------------------------------------------------------
# MISSING VALUE SUMMARY TABLE
# ---------------------------------------------------------

missing_summary = pd.DataFrame({
    "Column": df.columns,
    "Missing Count": missing_count.values,
    "Missing %": missing_percentage.values,
    "Data Type": df.dtypes.astype(str).values
})

missing_summary = (
    missing_summary[
        missing_summary["Missing Count"] > 0
    ]
    .sort_values(
        "Missing Count",
        ascending=False
    )
    .reset_index(drop=True)
)


# ---------------------------------------------------------
# TABLE
# ---------------------------------------------------------

st.subheader("Missing Value Summary")

st.dataframe(
    missing_summary,
    use_container_width=True
)


# ---------------------------------------------------------
# TOP 20 COLUMNS WITH MISSING VALUES
# ---------------------------------------------------------

st.subheader("Top 20 Columns with Missing Values")

top_20 = (
    missing_summary
    .head(20)
    .sort_values(
        "Missing Count",
        ascending=True
    )
)

fig_top_20 = px.bar(
    top_20,
    x="Missing Count",
    y="Column",
    orientation="h",
    title="Top 20 Columns with Missing Values",
    text="Missing Count"
)

st.plotly_chart(
    fig_top_20,
    use_container_width=True
)


# ---------------------------------------------------------
# MISSING PERCENTAGE BY COLUMN
# ---------------------------------------------------------

st.subheader("Missing Percentage by Column")

missing_percent_chart = (
    missing_summary
    .sort_values(
        "Missing %",
        ascending=False
    )
)

fig_percentage = px.bar(
    missing_percent_chart,
    x="Column",
    y="Missing %",
    title="Missing Percentage by Column",
    text="Missing %"
)

fig_percentage.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig_percentage,
    use_container_width=True
)


# ---------------------------------------------------------
# MISSING VALUES HEATMAP
# ---------------------------------------------------------

st.subheader("Missing Values Heatmap")

heatmap_columns = (
    missing_summary
    .head(20)["Column"]
    .tolist()
)

if heatmap_columns:

    heatmap_data = (
        df[heatmap_columns]
        .isna()
        .astype(int)
        .head(1000)
    )

    fig_heatmap = px.imshow(
        heatmap_data.T,
        aspect="auto",
        title="Missing Values Heatmap",
        labels={
            "x": "Rows",
            "y": "Columns",
            "color": "Missing"
        }
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )

else:

    st.info(
        "No missing values found in the dataset."
    )


# ---------------------------------------------------------
# MISSING VALUES BY DATA TYPE
# ---------------------------------------------------------

st.subheader("Missing Values by Data Type")

dtype_missing = (
    missing_summary
    .groupby("Data Type")["Missing Count"]
    .sum()
    .reset_index()
)

fig_dtype = px.bar(
    dtype_missing,
    x="Data Type",
    y="Missing Count",
    title="Missing Values by Data Type",
    text="Missing Count"
)

st.plotly_chart(
    fig_dtype,
    use_container_width=True
)


# ---------------------------------------------------------
# COLUMNS WITH MORE THAN 50% MISSING DATA
# ---------------------------------------------------------

st.subheader(
    "Columns with More Than 50% Missing Data"
)

over_50_table = (
    missing_summary[
        missing_summary["Missing %"] > 50
    ]
    .copy()
)

if not over_50_table.empty:

    st.dataframe(
        over_50_table,
        use_container_width=True
    )

else:

    st.success(
        "No columns contain more than 50% missing data."
    )


# ---------------------------------------------------------
# IMPORTANT ACTIONS
# ---------------------------------------------------------

st.subheader(
    "Recommended Missing Value Actions"
)

st.write(
    "For each column, decide whether to Drop, Fill with "
    "Mean, Fill with Median, Fill with Mode, Fill with "
    '"Unknown", or Create a Missing Indicator.'
)


# ---------------------------------------------------------
# SUGGEST ACTION
# ---------------------------------------------------------

def suggest_action(row):

    percentage = row["Missing %"]

    if percentage == 0:

        return "No Action"

    elif percentage > 50:

        return "Consider Drop"

    elif row["Data Type"] in [
        "object",
        "category"
    ]:

        return 'Fill with "Unknown" or Mode'

    elif percentage < 5:

        return "Fill with Mean / Median"

    elif percentage < 30:

        return "Fill with Median"

    else:
      
        return (
            "Fill with Median / "
            "Create Missing Indicator"
        )

action_table = missing_summary.copy()

action_table["Suggested Action"] = (
    action_table.apply(
        suggest_action,
        axis=1
    )
)

st.dataframe(
    action_table[
        [
            "Column",
            "Missing Count",
            "Missing %",
            "Data Type",
            "Suggested Action"
        ]
    ],
    use_container_width=True
)
