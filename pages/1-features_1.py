import streamlit as st
import pandas as pd

st.title('Features 1')
st.markdown("Hello world")


comp_name = pd.read_parquet("dataset/company_names.parquet")
st.dataframe(comp_name)