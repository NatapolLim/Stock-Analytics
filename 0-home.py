import streamlit as st
import yfinance as yf
import pandas as pd

from stock_analytics.config import get_setting_configs

st.title("Home")
# st.markdown("Hello world")

settings = get_setting_configs("dev")
tickers = settings["tickers"]

ticker = st.selectbox(
    label="Ticker",
    options=tickers,
)


def get_ticker(ticker: str) -> tuple[yf.Ticker, pd.DataFrame]:
    ticker = ticker + ".BK"
    ticker = yf.Ticker(ticker=ticker)
    return ticker


ticker = get_ticker(ticker)

history_price = ticker.history(period="5y", interval="1d")
st.line_chart(history_price.loc[:, "Close"])


balance_sheet_yearly_df = ticker.get_balance_sheet(pretty=True, freq="yearly")
balance_sheet_quarterly_df = ticker.get_balance_sheet(pretty=True, freq="quarterly")
cashflow_yearly_df = ticker.get_cashflow(pretty=True, freq="yearly")
cashflow_quarterly_df = ticker.get_cashflow(pretty=True, freq="quarterly")
income_yearly_df = ticker.get_incomestmt(pretty=True, freq="yearly")
income_quarterly_df = ticker.get_incomestmt(pretty=True, freq="quarterly")

financial_df = [
    balance_sheet_yearly_df,
    balance_sheet_quarterly_df,
    cashflow_yearly_df,
    cashflow_quarterly_df,
    income_yearly_df,
    income_quarterly_df,
]

for df in financial_df:
    df.fillna(0, inplace=True)

col_balance_sheet_quarterly_df = balance_sheet_quarterly_df.columns.strftime(
    date_format="%d-%m-%Y"
).values
col_balance_sheet_yearly_df = balance_sheet_yearly_df.columns.strftime(
    date_format="%d-%m-%Y"
).values
col_cashflow_yearly_df = cashflow_yearly_df.columns.strftime(
    date_format="%d-%m-%Y"
).values
col_cashflow_quarterly_df = cashflow_quarterly_df.columns.strftime(
    date_format="%d-%m-%Y"
).values

col_income_yearly_df = income_yearly_df.columns.strftime(date_format="%d-%m-%Y").values

col_income_quarterly_df = income_quarterly_df.columns.strftime(
    date_format="%d-%m-%Y"
).values

if balance_sheet_yearly_df.shape == (0, 0):
    st.markdown("No balance sheet data")

balance_sheet_yearly_df["Yearly"] = balance_sheet_yearly_df.agg(
    pd.Series.to_list, axis=1
)
balance_sheet_quarterly_df["Quarterly"] = balance_sheet_quarterly_df.agg(
    pd.Series.to_list, axis=1
)
cashflow_yearly_df["Yearly"] = cashflow_yearly_df.agg(pd.Series.to_list, axis=1)
cashflow_quarterly_df["Quarterly"] = cashflow_quarterly_df.agg(
    pd.Series.to_list, axis=1
)
income_yearly_df["Yearly"] = income_yearly_df.agg(pd.Series.to_list, axis=1)
income_quarterly_df["Quarterly"] = income_quarterly_df.agg(pd.Series.to_list, axis=1)

balance_sheet = pd.concat([balance_sheet_yearly_df, balance_sheet_quarterly_df], axis=1)
cashflow = pd.concat([cashflow_yearly_df, cashflow_quarterly_df], axis=1)
incomestmt = pd.concat([income_yearly_df, income_quarterly_df], axis=1)


tab1, tab2, tab3 = st.tabs(tabs=["Balance Sheet", "Cash Flow", "Income Statement"])

tab1.data_editor(
    balance_sheet[["Quarterly", "Yearly"]],
    column_config={
        "Quarterly": st.column_config.BarChartColumn(
            f"{col_balance_sheet_quarterly_df}",
        ),
        "Yearly": st.column_config.BarChartColumn(
            f"{col_balance_sheet_yearly_df}",
        ),
    },
    hide_index=False,
    use_container_width=True,
)

tab2.data_editor(
    cashflow[["Quarterly", "Yearly"]],
    column_config={
        "Quarterly": st.column_config.BarChartColumn(
            f"{col_cashflow_quarterly_df}",
        ),
        "Yearly": st.column_config.BarChartColumn(
            f"{col_cashflow_yearly_df}",
        ),
    },
    hide_index=False,
    use_container_width=True,
)

tab3.data_editor(
    incomestmt[["Quarterly", "Yearly"]],
    column_config={
        "Quarterly": st.column_config.BarChartColumn(
            f"{col_income_quarterly_df}",
        ),
        "Yearly": st.column_config.BarChartColumn(
            f"{col_income_yearly_df}",
        ),
    },
    hide_index=False,
    use_container_width=True,
)
