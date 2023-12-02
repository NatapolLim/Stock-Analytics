import streamlit as st
import pandas as pd


st.title('Home')
st.markdown("Hello world")

close_price = pd.read_parquet('dataset/close_price.parquet')
close_price.columns = pd.to_datetime(close_price.columns,)

symbols = close_price.index

temp_df = close_price.copy()
temp_df = temp_df.loc[:, '2023':]


list_price = []

for s in symbols:
    list_price.append([temp_df.loc[s].to_list()])

temp_df = pd.DataFrame(list_price, index=close_price.index)
print(temp_df)
st.dataframe(temp_df)

st.dataframe(
    temp_df,
    column_config={
        "symbol":"Symbol",
        '0': st.column_config.LineChartColumn(
            "Price",
            y_min=0,
        ),
    },
    )