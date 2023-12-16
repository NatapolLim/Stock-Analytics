import os
import yfinance as yf
import pandas as pd
from tqdm import tqdm

from prefect import task, flow
from stock_analytics.config import get_setting_configs

settings = get_setting_configs("dev")


@task(log_prints=True)
def preprocess_tickers(tickers: list[str]) -> list[str]:
    n_tick = len(tickers)
    tickers = list(map(lambda x: x.upper() + ".BK", settings.tickers))
    print(f"Number of symbols {n_tick}")

    return tickers


@task(log_prints=True)
def request_to_yfinance(
    tickers: list[str],
    period: str = "5y",
    interval: str = "1d",
    start_date: str = None,
) -> pd.DataFrame:
    tickers_ob = yf.Tickers(tickers)
    if start_date is not None:
        print(f"Getting update dataframe from {start_date}")
        df = tickers_ob.history(start=start_date, interval=interval)
    else:
        print(f"Getting dataframe {period} from yfinance")
        df = tickers_ob.history(period=period, interval=interval)

    return df


@task(log_prints=True)
def save_dataframe(
    df: pd.DataFrame,
    save_path: str,
) -> None:
    df.to_parquet(save_path)
    print(f"Saved to {save_path}")


@flow(name="initialize_data")
def initialize_data(
    tickers: list[str],
    backup_path: str,
    save_path: str,
):
    tickers = preprocess_tickers(tickers=tickers)
    df = request_to_yfinance(tickers=tickers)
    save_dataframe(df, backup_path)
    save_dataframe(df, save_path)


@flow(name="update_data")
def update_data(
    tickers: list[str],
    backup_path: str,
    save_path: str,
):
    tickers = preprocess_tickers(tickers=tickers)
    old_df = pd.read_parquet(backup_path)
    recent_date = old_df.index.max()
    print(f"Recent date {recent_date.strftime(format='%Y-%m-%d')}")

    df = request_to_yfinance(tickers=tickers, start_date=recent_date)
    print(f"Last data date {df.index.max().date()}")
    concat_df = pd.concat([old_df, df], axis=0)
    save_dataframe(concat_df, save_path)


if __name__ == "__main__":
    price_data_path = settings.dataset.price_path
    updated_price_data_path = settings.dataset.updated_price_path

    if not os.path.isfile(price_data_path):
        initialize_data(
            tickers=settings.tickers,
            backup_path=price_data_path,
            save_path=updated_price_data_path,
        )
    else:
        update_data(
            tickers=settings.tickers,
            backup_path=price_data_path,
            save_path=updated_price_data_path,
        )
