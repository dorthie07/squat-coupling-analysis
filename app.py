import streamlit as st
import pandas as pd
import numpy as np

st.title("Squat Physiological Data Analysis")

st.write(
    "Upload an Excel file containing time, heart rate, respiratory rate, "
    "SmO2, and THb data collected during a squat protocol."
)

uploaded_file = st.file_uploader(
    "Upload your Excel file",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("Your data")
    st.dataframe(df)

    st.write("Number of rows:", len(df))
    st.write("Number of columns:", len(df.columns))
