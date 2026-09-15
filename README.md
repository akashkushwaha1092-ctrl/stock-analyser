# Stock Analyser

A web platform that displays current stock prices, closing price charts, and trading volumes for multiple companies using Streamlit and Plotly.

## Features

- Multi-ticker selection (AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA and more)
- Interactive closing price chart (Plotly) — line or candlestick
- Interactive trading volume chart (Plotly)
- Per-ticker metrics cards with daily change percentage
- Configurable date range picker
- Chart type toggle (Line / Candlestick)

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://127.0.0.1:8501 in your browser.

## Tech Stack

- Streamlit
- Plotly
- yfinance
- pandas

## Usage

1. Select one or more tickers from the sidebar
2. Choose chart type (Line or Candlestick)
3. Adjust the date range if needed
4. View the closing price chart, volume chart, and metrics cards
