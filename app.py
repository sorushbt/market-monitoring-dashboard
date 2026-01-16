import streamlit as st
from datetime import datetime, timedelta
from data_loader import load_market_data

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

# Sanity checks
st.subheader("Data Overview")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**{asset_ticker}**")
    st.write(asset_data.tail())

with col2:
    st.write(f"**{benchmark_ticker}**")
    st.write(benchmark_data.tail())

