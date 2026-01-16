# Market Monitoring Dashboard

A professional trading-desk style dashboard for monitoring asset and benchmark performance, including risk metrics.

## Features

- API-based data ingestion from Yahoo Finance
- Cumulative performance vs benchmark
- Daily outperformance calculation
- Rolling 30-day volatility & Max Drawdown
- KPI indicators for quick overview
- Interactive Plotly charts in dark theme
- Sidebar for configurable tickers, date range and refresh

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sorushbt/market-monitoring-dashboard.git
```
2. Create a virtual environment and install dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

3. Run the dashboard:
   streamlit run app.py
