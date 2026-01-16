import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from data_loader import load_market_data
from metrics import (
    calculate_returns,
    calculate_cumulative_performance,
    calculate_outperformance
)


# Page config
st.set_page_config(page_title="Market Monitoring Dashboard", layout="wide")

st.title("Market Monitoring Dashboard")
st.caption("API-based market data ingestion and benchmark comparison")

# Sidebar - Configuration
st.sidebar.header("Market Configuration")

asset_ticker = st.sidebar.text_input("Asset ticker (Yahoo format)", "RHM.DE")

benchmark_ticker = st.sidebar.text_input("Benchmark ticker", value = "^GDAXI")

start_date = st.sidebar.date_input("Start date", value = datetime.today() - timedelta(days=365))

end_date = st.sidebar.date_input("End date", value = datetime.today())

# Data loading
with st.spinner("Loading market data..."):
    asset_data = load_market_data(asset_ticker, start_date, end_date)
    benchmark_data = load_market_data(benchmark_ticker, start_date, end_date)

# Performance Calculation
asset_returns = calculate_returns(asset_data)
benchmark_returns = calculate_returns(benchmark_data)

asset_cum_perf = calculate_cumulative_performance(asset_returns)
benchmark_cum_perf = calculate_cumulative_performance(benchmark_returns)

outperformance = calculate_outperformance(
    asset_returns,
    benchmark_returns,
)

# Sanity checks
st.subheader("Performance Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label = "Asset Cumulative Return",
        value = f"{asset_cum_perf.iloc[-1]:.2%}"
    )

with col2:
    st.metric(
        label = "Benchmark Cumulative Return",
        value = f"{benchmark_cum_perf.iloc[-1]:.2%}"
    )

with col3:
    st.metric(
        label = "Outperformance",
        value = f"{asset_cum_perf.iloc[-1] - benchmark_cum_perf.iloc[-1]:.2%}"
    )

st.subheader("Cumulative Performance Comparison")

performance_df = (
    pd.concat(
        [asset_cum_perf, benchmark_cum_perf],
        axis = 1
    )
)

performance_df.columns = [asset_ticker, benchmark_ticker]

st.line_chart(performance_df)