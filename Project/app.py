import streamlit as st
from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.features import create_features


st.set_page_config(
    page_title="Home Credit Default Risk",
    page_icon="🏠",
    layout="wide"
)

st.title("Home Credit Default Risk Analytics")

try:
    df = load_data()
    df = preprocess_data(df)
    df = create_features(df)

    st.success("Dataset loaded successfully!")

    st.write("Number of rows:", len(df))
    st.write("Number of columns:", len(df.columns))

    st.dataframe(df.head())

except FileNotFoundError:
    st.error("application_train.csv not found inside the data folder.")
