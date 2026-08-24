import streamlit as st

def sidebar_filters(df):
    st.sidebar.header("Filters")

    filters = {}

    if "TARGET" in df.columns:
        filters["target"] = st.sidebar.selectbox(
            "Default Status",
            ["All", "No Default", "Default"]
        )

    if "NAME_CONTRACT_TYPE" in df.columns:
        filters["contract_type"] = st.sidebar.multiselect(
            "Contract Type",
            df["NAME_CONTRACT_TYPE"].dropna().unique()
        )

    if "CODE_GENDER" in df.columns:
        filters["gender"] = st.sidebar.multiselect(
            "Gender",
            df["CODE_GENDER"].dropna().unique()
        )

    if "NAME_EDUCATION_TYPE" in df.columns:
        filters["education"] = st.sidebar.multiselect(
            "Education",
            df["NAME_EDUCATION_TYPE"].dropna().unique()
        )

    if "NAME_FAMILY_STATUS" in df.columns:
        filters["family_status"] = st.sidebar.multiselect(
            "Family Status",
            df["NAME_FAMILY_STATUS"].dropna().unique()
        )

    return filters


def apply_filters(df, filters):
    filtered_df = df.copy()

    if filters.get("target") == "No Default":
        filtered_df = filtered_df[filtered_df["TARGET"] == 0]

    elif filters.get("target") == "Default":
        filtered_df = filtered_df[filtered_df["TARGET"] == 1]

    if filters.get("contract_type"):
        filtered_df = filtered_df[
            filtered_df["NAME_CONTRACT_TYPE"].isin(filters["contract_type"])
        ]

    if filters.get("gender"):
        filtered_df = filtered_df[
            filtered_df["CODE_GENDER"].isin(filters["gender"])
        ]

    if filters.get("education"):
        filtered_df = filtered_df[
            filtered_df["NAME_EDUCATION_TYPE"].isin(filters["education"])
        ]

    if filters.get("family_status"):
        filtered_df = filtered_df[
            filtered_df["NAME_FAMILY_STATUS"].isin(filters["family_status"])
        ]

    return filtered_df
