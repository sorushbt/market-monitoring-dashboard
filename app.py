import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from data_loader import load_market_data
import plotly.express as px
import plotly.graph_objects as go
from metrics import (
    calculate_returns,
    calculate_cumulative_performance,
    calculate_outperformance, calculate_rolling_volatility, calculate_max_drawdown
)

# Page config
st.set_page_config(page_title="Market Monitoring Dashboard", layout="wide", initial_sidebar_state="expanded")

st.title("Market Monitoring Dashboard")
st.caption("Operational view: Asset vs Benchmark Performance & Risk Metrics")

# Sidebar - Configuration
st.sidebar.header("Market Configuration")

st.sidebar.markdown(
    "Configure the asset, benchmark and data range.\n"
    "Ticker symbols must watch Yahoo Finance format.")

asset_ticker = st.sidebar.text_input(
    "Asset ticker",
    value = "RHM.DE",
    help = "Ticker of the asset (e.g. RHM.DE)")

benchmark_ticker = st.sidebar.text_input(
    "Benchmark ticker",
    value = "^GDAXI",
    help = "Benchmark index (e.g. ^GDAXI for DAX)")

start_date = st.sidebar.date_input(
    "Start date",
    value = datetime.today() - timedelta(days=365))

end_date = st.sidebar.date_input(
    "End date",
    value = datetime.today(),
    help = "End date for historical data")

if st.sidebar.button("Refresh Data"):
    st.experimental_rerun()

# Data loading
with st.spinner("Loading market data..."):
    try:
        asset_data = load_market_data(asset_ticker, start_date, end_date)
        benchmark_data = load_market_data(benchmark_ticker, start_date, end_date)
    except ValueError as e:
        st.error(f"Data load error: {e}")
        st.stop()

# Performance Calculation
asset_returns = calculate_returns(asset_data)
benchmark_returns = calculate_returns(benchmark_data)

asset_cum_perf = calculate_cumulative_performance(asset_returns)
benchmark_cum_perf = calculate_cumulative_performance(benchmark_returns)
outperformance = calculate_outperformance(asset_returns, benchmark_returns)

rolling_vol = calculate_rolling_volatility(asset_returns)
max_dd = calculate_max_drawdown(asset_cum_perf)

# KPI panels
st.subheader("Key Performance & Risk Metrics")

kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.metric("Asset Cumulative Return", f"{asset_cum_perf.iloc[-1]:.2%}")

with kpi_cols[1]:
    st.metric("Benchmark Cumulative Return", f"{benchmark_cum_perf.iloc[-1]:.2%}")

with kpi_cols[2]:
    st.metric("Outperformance", f"{(asset_cum_perf.iloc[-1] - benchmark_cum_perf.iloc[-1]):.2%}")

with kpi_cols[3]:
    st.metric("Rolling Volatility (Annualized)", f"{rolling_vol.iloc[-1]:.2%}")

# Chart Tabs
tab1, tab2 = st.tabs(["Performance Charts", "Risk Metrics"])

# Performance Charts
with tab1:
    st.subheader("Cumulative Performance vs Benchmark")
    cum_df = pd.concat([asset_cum_perf, benchmark_cum_perf], axis = 1)
    cum_df.columns = [asset_ticker, benchmark_ticker]
    cum_df.reset_index(inplace = True)

    fig_cum = px.line(
        cum_df,
        x = "Date",
        y = [asset_ticker, benchmark_ticker],
        template = "plotly_dark",
        title = "Cumulative Performance vs Benchmark",
        labels = {"value": "Cumulative Return", "variable": "Ticker"}
    )
    fig_cum.update_traces(mode = "lines+markers")
    st.plotly_chart(fig_cum, use_container_width = True)

# Risk Metrics Charts
with tab2:
    st.subheader("Rolling 30-Day Volatility")
    vol_df = rolling_vol.to_frame(name = "Volatility")
    vol_df.reset_index(inplace = True)

    fig_vol = px.line(
        vol_df,
        x = "Date",
        y = "Volatility",
        template = "plotly_dark",
        title = "Rolling 30-Day Volatility (Annualized)",
        labels = {"Volatility": "Volatility"}
    )
    fig_vol.update_traces(mode = "lines+markers")
    st.plotly_chart(fig_vol, use_container_width = True)

    st.markdown(f"**Max Drawdown:** {max_dd:.2%}")

# Outperformance Chart
st.subheader("Daily Outperformance vs Benchmark")
out_df = outperformance.to_frame(name = "Outperformance")
out_df.reset_index(inplace = True)
fig_out = px.bar(
    out_df,
    x = "Date",
    y = "Outperformance",
    template = "plotly_dark",
    title = "Daily Outperformance vs Benchmark",
    labels = {"Outperformance": "Relative Return"}
)

st.plotly_chart(fig_out, use_container_width = True)