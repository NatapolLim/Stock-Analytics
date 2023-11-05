import yfinance as yf
import pandas as pd
from tqdm import tqdm

from stock_analytics import logger

def request_all_history_data_from_yf(
        period,
        interval,
        ) -> pd.DataFrame :
    
    company_names = pd.read_parquet('./dataset/company_names.parquet')
    company_names = company_names[company_names.market=='SET']

    all_df=[]
    for name in tqdm(company_names.name):
        name_bk = f"{name.upper()}.BK"
        stock = yf.Ticker(name_bk)
        df = stock.history(period=period, interval=interval)
        df['symbol'] = name

        # logger.info(f"Download {name_bk}")

        all_df.append(df)

    return pd.concat(all_df, axis=0)

