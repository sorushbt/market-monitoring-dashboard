from itertools import starmap

import yfinance as yf
import pandas as pd
from datetime import date

def load_market_data(
        ticker: str,
        start: date,
        end: date,
) -> pd.DataFrame:

    df = yf.download(
        ticker,
        start = start,
        end = end,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No data returned for ticker {ticker}")

    # Normalize column names
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.dropna(inplace=True)

    return df
