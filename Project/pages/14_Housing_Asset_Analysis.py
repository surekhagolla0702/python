import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Housing & Asset Analysis",
    page_icon="🏠",
    layout="wide"
)

st.title("Housing & Asset Analysis")

st.write(
    "Analyze property and vehicle ownership."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()
df = preprocess_data(df)
df = create_features(df)


# ---------------------------------------------------------
# CLEAN OWNERSHIP COLUMNS
# ---------------------------------------------------------

df["CAR_OWNERSHIP"] = df["FLAG_OWN_CAR"].map({
    "Y": "Owns Car",
    "N": "Does Not Own Car"
})

df["PROPERTY_OWNERSHIP"] = df["FLAG_OWN_REALTY"].map({
    "Y": "Owns Property",
    "N": "Does Not Own Property"
})


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

car_owners = (
    df["FLAG_OWN_CAR"] == "Y"
).sum()

property_owners = (
    df["FLAG_OWN_REALTY"] == "Y"
).sum()

customers_owning_both = (
    (df["FLAG_OWN_CAR"] == "Y") &
    (df["FLAG_OWN_REALTY"] == "Y")
).sum()

property_owner_default_rate = (
    df.loc[
        df["FLAG_OWN_REALTY"] == "Y",
        "TARGET"
    ].mean() * 100
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("KPI Cards")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Car Owners",
    f"{car_owners:,}"
)

col2.metric(
    "Property Owners",
    f"{property_owners:,}"
)

col3.metric(
    "Customers Owning Both",
    f"{customers_owning_both:,}"
)

col4.metric(
    "Default Rate of Property Owners",
    f"{property_owner_default_rate:.2f}%"
)


# ---------------------------------------------------------
# CAR OWNERSHIP DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Car Ownership Distribution")

car_distribution = (
    df["CAR_OWNERSHIP"]
    .dropna()
    .value_counts()
    .reset_index()
)

car_distribution.columns = [
    "Car Ownership",
    "Customers"
]

fig_car = px.pie(
    car_distribution,
    names="Car Ownership",
    values="Customers",
    title="Car Ownership Distribution"
)

st.plotly_chart(
    fig_car,
    use_container_width=True
)


# ---------------------------------------------------------
# PROPERTY OWNERSHIP DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Property Ownership Distribution")

property_distribution = (
    df["PROPERTY_OWNERSHIP"]
    .dropna()
    .value_counts()
    .reset_index()
)

property_distribution.columns = [
    "Property Ownership",
    "Customers"
]

fig_property = px.pie(
    property_distribution,
    names="Property Ownership",
    values="Customers",
    title="Property Ownership Distribution"
)

st.plotly_chart(
    fig_property,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY CAR OWNERSHIP
# ---------------------------------------------------------

st.subheader("Default Rate by Car Ownership")

car_default = (
    df.dropna(subset=["CAR_OWNERSHIP"])
    .groupby("CAR_OWNERSHIP")["TARGET"]
    .mean()
    .reset_index()
)

car_default["Default Rate (%)"] = (
    car_default["TARGET"] * 100
)

fig_car_default = px.bar(
    car_default,
    x="CAR_OWNERSHIP",
    y="Default Rate (%)",
    title="Default Rate by Car Ownership",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_car_default,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY PROPERTY OWNERSHIP
# ---------------------------------------------------------

st.subheader("Default Rate by Property Ownership")

property_default = (
    df.dropna(subset=["PROPERTY_OWNERSHIP"])
    .groupby("PROPERTY_OWNERSHIP")["TARGET"]
    .mean()
    .reset_index()
)

property_default["Default Rate (%)"] = (
    property_default["TARGET"] * 100
)

fig_property_default = px.bar(
    property_default,
    x="PROPERTY_OWNERSHIP",
    y="Default Rate (%)",
    title="Default Rate by Property Ownership",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_property_default,
    use_container_width=True
)


# ---------------------------------------------------------
# APPLICANTS BY HOUSING TYPE
# ---------------------------------------------------------

st.subheader("Applicants by Housing Type")

housing_count = (
    df["NAME_HOUSING_TYPE"]
    .dropna()
    .value_counts()
    .reset_index()
)

housing_count.columns = [
    "Housing Type",
    "Applicants"
]

fig_housing = px.bar(
    housing_count,
    x="Housing Type",
    y="Applicants",
    title="Applicants by Housing Type",
    text="Applicants"
)

st.plotly_chart(
    fig_housing,
    use_container_width=True
)


# ---------------------------------------------------------
# DEFAULT RATE BY HOUSING TYPE
# ---------------------------------------------------------

st.subheader("Default Rate by Housing Type")

housing_default = (
    df.dropna(subset=["NAME_HOUSING_TYPE"])
    .groupby("NAME_HOUSING_TYPE")["TARGET"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

housing_default["Default Rate (%)"] = (
    housing_default["TARGET"] * 100
)

fig_housing_default = px.bar(
    housing_default,
    x="NAME_HOUSING_TYPE",
    y="Default Rate (%)",
    title="Default Rate by Housing Type",
    text="Default Rate (%)"
)

st.plotly_chart(
    fig_housing_default,
    use_container_width=True
)


# ---------------------------------------------------------
# AVERAGE CREDIT BY HOUSING TYPE
# ---------------------------------------------------------

st.subheader("Average Credit by Housing Type")

housing_credit = (
    df.dropna(subset=["NAME_HOUSING_TYPE"])
    .groupby("NAME_HOUSING_TYPE")["AMT_CREDIT"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

housing_credit.columns = [
    "Housing Type",
    "Average Credit"
]

fig_credit = px.bar(
    housing_credit,
    x="Housing Type",
    y="Average Credit",
    title="Average Credit by Housing Type",
    text="Average Credit"
)

st.plotly_chart(
    fig_credit,
    use_container_width=True
)
