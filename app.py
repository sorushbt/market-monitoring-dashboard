import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 Market Monitoring Dashboard")

ticker = st.text_input("Ticker (Yahoo format)", "SAP.DE")

# Marktdaten laden (yfinance)
@st.cache_data
def load_data(ticker):
    return yf.download(ticker, period="6mo")

data = load_data(ticker)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        return df

data = normalize_columns(data)

st.write("Preview of market data")
st.dataframe(data.head())

# Returns- & Volatilitätsanalyse
data["Daily Return %"] = data["Close"].pct_change() * 100
data["Rolling Volatility %"] = data["Daily Return %"].rolling(5).std()

st.subheader("Market Metrics")
st.write(data[["Close", "Daily Return %", "Rolling Volatility %"]].tail())

# Visualisierung mit Plotly
import plotly.express as px

fig = px.line(
        data,
        x = data.index,
        y = "Close",
        title = "Closing Price"
            )

st.plotly_chart(fig, use_container_width=True)