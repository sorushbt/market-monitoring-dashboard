import pandas as pd

def calculate_returns(data: pd.DataFrame) -> pd.Series:
    returns = data["Close"].pct_change()
    return returns.dropna()

def calculate_cumulative_performance(returns: pd.Series) -> pd.Series:
    cumulative = (1 + returns).cumprod() - 1
    return cumulative

def calculate_outperformance(
        asset_returns: pd.Series,
        benchmark_returns: pd.Series
) -> pd.Series:

    aligned = pd.concat(
        [asset_returns, benchmark_returns],
        axis = 1,
        join = "inner",
    )

    aligned.columns = ["asset", "benchmark"]

    return aligned["asset"] - aligned["benchmark"]

def calculate_rolling_volatility(returns: pd.Series, window: int = 30) -> pd.Series:
    return returns.rolling(window = window).std() * (252 ** 0.5)

def calculate_max_drawdown(cum_perf: pd.Series) -> float:
    roll_max = cum_perf.cummax()
    drawdown = (cum_perf - roll_max)
    max_dd = drawdown.min()

    return max_dd