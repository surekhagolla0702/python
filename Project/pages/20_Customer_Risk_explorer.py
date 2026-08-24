import streamlit as st
import pandas as pd
import numpy as np

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Customer Risk Explorer",
    page_icon="👤",
    layout="wide"
)

st.title("Customer Risk Explorer")

st.write(
    "Explore individual customers and filtered applicant records "
    "to understand customer-level credit risk."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)
df = create_features(df)


# ---------------------------------------------------------
# CREATE DERIVED FEATURES
# ---------------------------------------------------------

if "DAYS_BIRTH" in df.columns:
    df["AGE"] = (
        df["DAYS_BIRTH"].abs() / 365
    )

if "DAYS_EMPLOYED" in df.columns:
    df["EMPLOYMENT_YEARS"] = (
        df["DAYS_EMPLOYED"].abs() / 365
    )

if (
    "AMT_CREDIT" in df.columns
    and "AMT_INCOME_TOTAL" in df.columns
):
    df["CREDIT_INCOME_RATIO"] = (
        df["AMT_CREDIT"] /
        df["AMT_INCOME_TOTAL"].replace(0, np.nan)
    )

if (
    "AMT_ANNUITY" in df.columns
    and "AMT_INCOME_TOTAL" in df.columns
):
    df["ANNUITY_INCOME_RATIO"] = (
        df["AMT_ANNUITY"] /
        df["AMT_INCOME_TOTAL"].replace(0, np.nan)
    )

if (
    "AMT_CREDIT" in df.columns
    and "AMT_GOODS_PRICE" in df.columns
):
    df["CREDIT_GOODS_RATIO"] = (
        df["AMT_CREDIT"] /
        df["AMT_GOODS_PRICE"].replace(0, np.nan)
    )

external_columns = [
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3"
]

available_external_columns = [
    column
    for column in external_columns
    if column in df.columns
]

if available_external_columns:
    df["AVERAGE_EXTERNAL_SCORE"] = (
        df[available_external_columns].mean(axis=1)
    )


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("Customer Filters")


# ---------------------------------------------------------
# TARGET FILTER
# ---------------------------------------------------------

if "TARGET" in df.columns:

    target_options = st.sidebar.multiselect(
        "TARGET",
        options=sorted(df["TARGET"].dropna().unique()),
        default=sorted(df["TARGET"].dropna().unique())
    )

else:

    target_options = []


# ---------------------------------------------------------
# GENDER FILTER
# ---------------------------------------------------------

gender_column = "CODE_GENDER"

if gender_column in df.columns:

    gender_options = st.sidebar.multiselect(
        "Gender",
        options=sorted(
            df[gender_column]
            .dropna()
            .astype(str)
            .unique()
        ),
        default=sorted(
            df[gender_column]
            .dropna()
            .astype(str)
            .unique()
        )
    )

else:

    gender_options = []


# ---------------------------------------------------------
# AGE FILTER
# ---------------------------------------------------------

if "AGE" in df.columns:

    age_min = int(
        np.floor(df["AGE"].min())
    )

    age_max = int(
        np.ceil(df["AGE"].max())
    )

    age_range = st.sidebar.slider(
        "Age Range",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max)
    )

else:

    age_range = None


# ---------------------------------------------------------
# INCOME RANGE
# ---------------------------------------------------------

if "AMT_INCOME_TOTAL" in df.columns:

    income_min = float(
        df["AMT_INCOME_TOTAL"].min()
    )

    income_max = float(
        df["AMT_INCOME_TOTAL"].max()
    )

    income_range = st.sidebar.slider(
        "Income Range",
        min_value=income_min,
        max_value=income_max,
        value=(income_min, income_max)
    )

else:

    income_range = None


# ---------------------------------------------------------
# CREDIT RANGE
# ---------------------------------------------------------

if "AMT_CREDIT" in df.columns:

    credit_min = float(
        df["AMT_CREDIT"].min()
    )

    credit_max = float(
        df["AMT_CREDIT"].max()
    )

    credit_range = st.sidebar.slider(
        "Credit Range",
        min_value=credit_min,
        max_value=credit_max,
        value=(credit_min, credit_max)
    )

else:

    credit_range = None


# ---------------------------------------------------------
# INCOME TYPE
# ---------------------------------------------------------

income_type_column = "NAME_INCOME_TYPE"

if income_type_column in df.columns:

    income_type_options = st.sidebar.multiselect(
        "Income Type",
        options=sorted(
            df[income_type_column]
            .dropna()
            .astype(str)
            .unique()
        )
    )

else:

    income_type_options = []


# ---------------------------------------------------------
# EDUCATION
# ---------------------------------------------------------

education_column = "NAME_EDUCATION_TYPE"

if education_column in df.columns:

    education_options = st.sidebar.multiselect(
        "Education",
        options=sorted(
            df[education_column]
            .dropna()
            .astype(str)
            .unique()
        )
    )

else:

    education_options = []


# ---------------------------------------------------------
# OCCUPATION
# ---------------------------------------------------------

occupation_column = "OCCUPATION_TYPE"

if occupation_column in df.columns:

    occupation_options = st.sidebar.multiselect(
        "Occupation",
        options=sorted(
            df[occupation_column]
            .dropna()
            .astype(str)
            .unique()
        )
    )

else:

    occupation_options = []


# ---------------------------------------------------------
# CONTRACT TYPE
# ---------------------------------------------------------

contract_column = "NAME_CONTRACT_TYPE"

if contract_column in df.columns:

    contract_options = st.sidebar.multiselect(
        "Contract Type",
        options=sorted(
            df[contract_column]
            .dropna()
            .astype(str)
            .unique()
        )
    )

else:

    contract_options = []


# ---------------------------------------------------------
# HOUSING TYPE
# ---------------------------------------------------------

housing_column = "NAME_HOUSING_TYPE"

if housing_column in df.columns:

    housing_options = st.sidebar.multiselect(
        "Housing Type",
        options=sorted(
            df[housing_column]
            .dropna()
            .astype(str)
            .unique()
        )
    )

else:

    housing_options = []


# ---------------------------------------------------------
# CAR OWNERSHIP
# ---------------------------------------------------------

car_column = "FLAG_OWN_CAR"

if car_column in df.columns:

    car_options = st.sidebar.multiselect(
        "Car Ownership",
        options=sorted(
            df[car_column]
            .dropna()
            .astype(str)
            .unique()
        )
    )

else:

    car_options = []


# ---------------------------------------------------------
# PROPERTY OWNERSHIP
# ---------------------------------------------------------

property_column = "FLAG_OWN_REALTY"

if property_column in df.columns:

    property_options = st.sidebar.multiselect(
        "Property Ownership",
        options=sorted(
            df[property_column]
            .dropna()
            .astype(str)
            .unique()
        )
    )

else:

    property_options = []


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df.copy()


if "TARGET" in df.columns and target_options:

    filtered_df = filtered_df[
        filtered_df["TARGET"].isin(target_options)
    ]


if gender_column in df.columns and gender_options:

    filtered_df = filtered_df[
        filtered_df[gender_column]
        .astype(str)
        .isin(gender_options)
    ]


if "AGE" in df.columns and age_range is not None:

    filtered_df = filtered_df[
        filtered_df["AGE"].between(
            age_range[0],
            age_range[1]
        )
    ]


if (
    "AMT_INCOME_TOTAL" in df.columns
    and income_range is not None
):

    filtered_df = filtered_df[
        filtered_df["AMT_INCOME_TOTAL"].between(
            income_range[0],
            income_range[1]
        )
    ]


if (
    "AMT_CREDIT" in df.columns
    and credit_range is not None
):

    filtered_df = filtered_df[
        filtered_df["AMT_CREDIT"].between(
            credit_range[0],
            credit_range[1]
        )
    ]


if income_type_column in df.columns and income_type_options:

    filtered_df = filtered_df[
        filtered_df[income_type_column]
        .astype(str)
        .isin(income_type_options)
    ]


if education_column in df.columns and education_options:

    filtered_df = filtered_df[
        filtered_df[education_column]
        .astype(str)
        .isin(education_options)
    ]


if occupation_column in df.columns and occupation_options:

    filtered_df = filtered_df[
        filtered_df[occupation_column]
        .astype(str)
        .isin(occupation_options)
    ]


if contract_column in df.columns and contract_options:

    filtered_df = filtered_df[
        filtered_df[contract_column]
        .astype(str)
        .isin(contract_options)
    ]


if housing_column in df.columns and housing_options:

    filtered_df = filtered_df[
        filtered_df[housing_column]
        .astype(str)
        .isin(housing_options)
    ]


if car_column in df.columns and car_options:

    filtered_df = filtered_df[
        filtered_df[car_column]
        .astype(str)
        .isin(car_options)
    ]


if property_column in df.columns and property_options:

    filtered_df = filtered_df[
        filtered_df[property_column]
        .astype(str)
        .isin(property_options)
    ]


# ---------------------------------------------------------
# SEARCH CUSTOMER ID
# ---------------------------------------------------------

st.subheader("Search Customer")

search_id = st.text_input(
    "Search using SK_ID_CURR",
    placeholder="Enter Customer ID"
)


search_df = filtered_df.copy()


if search_id:

    if "SK_ID_CURR" in search_df.columns:

        search_df = search_df[
            search_df["SK_ID_CURR"]
            .astype(str)
            .str.contains(
                search_id.strip(),
                case=False,
                na=False
            )
        ]

    else:

        st.warning(
            "SK_ID_CURR column is not available."
        )


# ---------------------------------------------------------
# CUSTOMER RISK PROFILE
# ---------------------------------------------------------

st.subheader("Customer Risk Profile")


if search_id and not search_df.empty:

    customer = search_df.iloc[0]

    profile_columns = st.columns(4)

    # Customer ID
    with profile_columns[0]:

        if "SK_ID_CURR" in search_df.columns:
            st.metric(
                "Customer ID",
                str(customer["SK_ID_CURR"])
            )

        if "TARGET" in search_df.columns:
            st.metric(
                "TARGET",
                str(customer["TARGET"])
            )

    # Age and Gender
    with profile_columns[1]:

        if "AGE" in search_df.columns:
            st.metric(
                "Age",
                f"{customer['AGE']:.1f} years"
            )

        if gender_column in search_df.columns:
            st.write(
                f"**Gender:** {customer[gender_column]}"
            )

    # Income and Credit
    with profile_columns[2]:

        if "AMT_INCOME_TOTAL" in search_df.columns:
            st.metric(
                "Income",
                f"{customer['AMT_INCOME_TOTAL']:,.0f}"
            )

        if "AMT_CREDIT" in search_df.columns:
            st.metric(
                "Credit Amount",
                f"{customer['AMT_CREDIT']:,.0f}"
            )

    # Annuity
    with profile_columns[3]:

        if "AMT_ANNUITY" in search_df.columns:
            st.metric(
                "Annuity",
                f"{customer['AMT_ANNUITY']:,.0f}"
            )


    st.markdown("---")


    # -----------------------------------------------------
    # CUSTOMER DETAILS
    # -----------------------------------------------------

    detail_col1, detail_col2 = st.columns(2)


    with detail_col1:

        if education_column in search_df.columns:
            st.write(
                f"**Education:** "
                f"{customer[education_column]}"
            )

        if occupation_column in search_df.columns:
            st.write(
                f"**Occupation:** "
                f"{customer[occupation_column]}"
            )

        if "NAME_FAMILY_STATUS" in search_df.columns:
            st.write(
                f"**Family Status:** "
                f"{customer['NAME_FAMILY_STATUS']}"
            )

        if "CNT_CHILDREN" in search_df.columns:
            st.write(
                f"**Number of Children:** "
                f"{customer['CNT_CHILDREN']}"
            )

        if housing_column in search_df.columns:
            st.write(
                f"**Housing Type:** "
                f"{customer[housing_column]}"
            )


    with detail_col2:

        if "EXT_SOURCE_1" in search_df.columns:
            st.write(
                f"**External Score 1:** "
                f"{customer['EXT_SOURCE_1']:.3f}"
                if pd.notna(customer["EXT_SOURCE_1"])
                else "**External Score 1:** N/A"
            )

        if "EXT_SOURCE_2" in search_df.columns:
            st.write(
                f"**External Score 2:** "
                f"{customer['EXT_SOURCE_2']:.3f}"
                if pd.notna(customer["EXT_SOURCE_2"])
                else "**External Score 2:** N/A"
            )

        if "EXT_SOURCE_3" in search_df.columns:
            st.write(
                f"**External Score 3:** "
                f"{customer['EXT_SOURCE_3']:.3f}"
                if pd.notna(customer["EXT_SOURCE_3"])
                else "**External Score 3:** N/A"
            )


    # -----------------------------------------------------
    # CALCULATED RISK INDICATORS
    # -----------------------------------------------------

    st.subheader("Calculated Risk Indicators")

    risk_col1, risk_col2, risk_col3, risk_col4, risk_col5 = (
        st.columns(5)
    )


    with risk_col1:

        if "CREDIT_INCOME_RATIO" in search_df.columns:

            value = customer["CREDIT_INCOME_RATIO"]

            if pd.notna(value):

                st.metric(
                    "Credit-to-Income Ratio",
                    f"{value:.2f}"
                )

            else:

                st.metric(
                    "Credit-to-Income Ratio",
                    "N/A"
                )


    with risk_col2:

        if "ANNUITY_INCOME_RATIO" in search_df.columns:

            value = customer["ANNUITY_INCOME_RATIO"]

            if pd.notna(value):

                st.metric(
                    "Annuity-to-Income Ratio",
                    f"{value:.2f}"
                )

            else:

                st.metric(
                    "Annuity-to-Income Ratio",
                    "N/A"
                )


    with risk_col3:

        if "CREDIT_GOODS_RATIO" in search_df.columns:

            value = customer["CREDIT_GOODS_RATIO"]

            if pd.notna(value):

                st.metric(
                    "Credit-to-Goods Ratio",
                    f"{value:.2f}"
                )

            else:

                st.metric(
                    "Credit-to-Goods Ratio",
                    "N/A"
                )


    with risk_col4:

        if "EMPLOYMENT_YEARS" in search_df.columns:

            value = customer["EMPLOYMENT_YEARS"]

            if pd.notna(value):

                st.metric(
                    "Employment Years",
                    f"{value:.1f}"
                )

            else:

                st.metric(
                    "Employment Years",
                    "N/A"
                )


    with risk_col5:

        if "AVERAGE_EXTERNAL_SCORE" in search_df.columns:

            value = customer["AVERAGE_EXTERNAL_SCORE"]

            if pd.notna(value):

                st.metric(
                    "Average External Score",
                    f"{value:.3f}"
                )

            else:

                st.metric(
                    "Average External Score",
                    "N/A"
                )


elif search_id and search_df.empty:

    st.warning(
        "No customer found matching the search and selected filters."
    )

else:

    st.info(
        "Enter a Customer ID above to view the customer risk profile."
    )


# ---------------------------------------------------------
# FILTERED APPLICANT RECORDS
# ---------------------------------------------------------

st.subheader("Filtered Applicant Records")

st.write(
    f"Showing **{len(filtered_df):,}** applicant records."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)


# ---------------------------------------------------------
# DOWNLOAD FILTERED CUSTOMERS
# ---------------------------------------------------------

st.subheader("Download Options")


filtered_csv = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Filtered Customers",
    data=filtered_csv,
    file_name="filtered_customers.csv",
    mime="text/csv"
)


# ---------------------------------------------------------
# DOWNLOAD DEFAULT CUSTOMERS
# ---------------------------------------------------------

if "TARGET" in df.columns:

    default_df = df[
        df["TARGET"] == 1
    ].copy()

    default_csv = default_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Default Customers",
        data=default_csv,
        file_name="default_customers.csv",
        mime="text/csv"
    )


# ---------------------------------------------------------
# HIGH-RISK CUSTOMERS
# ---------------------------------------------------------

high_risk_df = df.copy()


if "CREDIT_INCOME_RATIO" in high_risk_df.columns:

    credit_ratio_threshold = (
        high_risk_df["CREDIT_INCOME_RATIO"]
        .quantile(0.75)
    )

else:

    credit_ratio_threshold = np.nan


if "ANNUITY_INCOME_RATIO" in high_risk_df.columns:

    annuity_ratio_threshold = (
        high_risk_df["ANNUITY_INCOME_RATIO"]
        .quantile(0.75)
    )

else:

    annuity_ratio_threshold = np.nan


if "AVERAGE_EXTERNAL_SCORE" in high_risk_df.columns:

    external_score_threshold = (
        high_risk_df["AVERAGE_EXTERNAL_SCORE"]
        .quantile(0.25)
    )

else:

    external_score_threshold = np.nan


high_risk_conditions = pd.Series(
    False,
    index=high_risk_df.index
)


if "CREDIT_INCOME_RATIO" in high_risk_df.columns:

    high_risk_conditions = (
        high_risk_conditions
        | (
            high_risk_df["CREDIT_INCOME_RATIO"]
            >= credit_ratio_threshold
        )
    )


if "ANNUITY_INCOME_RATIO" in high_risk_df.columns:

    high_risk_conditions = (
        high_risk_conditions
        | (
            high_risk_df["ANNUITY_INCOME_RATIO"]
            >= annuity_ratio_threshold
        )
    )


if "AVERAGE_EXTERNAL_SCORE" in high_risk_df.columns:

    high_risk_conditions = (
        high_risk_conditions
        | (
            high_risk_df["AVERAGE_EXTERNAL_SCORE"]
            <= external_score_threshold
        )
    )


if "TARGET" in high_risk_df.columns:

    high_risk_conditions = (
        high_risk_conditions
        | (high_risk_df["TARGET"] == 1)
    )


high_risk_df = high_risk_df[
    high_risk_conditions
].copy()


# ---------------------------------------------------------
# DOWNLOAD HIGH-RISK CUSTOMERS
# ---------------------------------------------------------

high_risk_csv = high_risk_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download High-Risk Customers",
    data=high_risk_csv,
    file_name="high_risk_customers.csv",
    mime="text/csv"
)


# ---------------------------------------------------------
# SUMMARY CSV
# ---------------------------------------------------------

summary_data = {
    "Metric": [
        "Total Applications",
        "Filtered Applications",
        "Default Customers",
        "High-Risk Customers"
    ],
    "Value": [
        len(df),
        len(filtered_df),
        (
            int((df["TARGET"] == 1).sum())
            if "TARGET" in df.columns
            else 0
        ),
        len(high_risk_df)
    ]
}

summary_df = pd.DataFrame(
    summary_data
)


summary_csv = summary_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Summary CSV",
    data=summary_csv,
    file_name="customer_risk_summary.csv",
    mime="text/csv"
)
