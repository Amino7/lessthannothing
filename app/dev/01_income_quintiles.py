import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Income quintiles — lessthannothing",
    page_icon="▮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("## Income distribution by quintile")
st.write(
    "This page will show how income is distributed across population quintiles "
    "for the selected countries over time."
)

@st.cache_data
def load_quintiles() -> pd.DataFrame:
    return pd.read_parquet("data/core/fact_income_quintiles.parquet")

try:
    df = load_quintiles()
    st.write("Preview of processed income‑quintiles data:")
    st.dataframe(df.head())
except FileNotFoundError:
    st.warning(
        "Processed income‑quintiles data not found yet. "
        "Once you create `data/core/fact_income_quintiles.parquet`, "
        "it will appear here."
    )
