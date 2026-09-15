import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Price Platform", layout="wide")

DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"]

END_DATE = datetime.today()
START_DATE = END_DATE - timedelta(days=365)

st.title("📈 Stock Price Platform")

col1, col2 = st.columns(2)

with col1:
    selected_tickers = st.multiselect(
        "Select Companies",
        options=DEFAULT_TICKERS,
        default=["AAPL", "GOOGL"],
    )

with col2:
    chart_type = st.selectbox(
        "Chart Type",
        options=["Line", "Candlestick"],
        index=0,
    )

start_date = st.date_input(
    "Start Date",
    value=START_DATE,
    key="start_date",
)

end_date = st.date_input(
    "End Date",
    value=END_DATE,
    key="end_date",
)

if selected_tickers:
    data_map = {}
    for ticker in selected_tickers:
        try:
            df = yf.download(ticker, start=pd.to_datetime(start_date), end=pd.to_datetime(end_date), progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel("Ticker")
            if not df.empty:
                data_map[ticker] = df
        except Exception as e:
            st.warning(f"Error fetching {ticker}: {e}")
            continue

    if data_map:
        metrics_col = st.columns(len(data_map))
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]

        for i, (ticker, df) in enumerate(data_map.items()):
            with metrics_col[i]:
                latest_close = df["Close"].iloc[-1]
                prev_close = df["Close"].iloc[-2] if len(df) > 1 else latest_close
                daily_change = ((latest_close - prev_close) / prev_close) * 100 if prev_close else 0
                change_symbol = "▲" if daily_change >= 0 else "▼"
                bg = "linear-gradient(135deg, #28a745, #34ce57)" if daily_change >= 0 else "linear-gradient(135deg, #dc3545, #e4606d)"
                st.markdown(
                    f"""
                    <div style="background: {bg}; border-radius: 12px; padding: 16px; color: white; text-align: center;">
                        <h4 style="margin: 4px 0;">{ticker}</h4>
                        <h2 style="margin: 4px 0;">${latest_close:,.2f}</h2>
                        <p style="margin: 4px 0; font-weight: bold;">{change_symbol} {abs(daily_change):.2f}%</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        price_traces = []
        volume_traces = []

        for i, ticker in enumerate(data_map.keys()):
            df = data_map[ticker]
            color = colors[i % len(colors)]

            if chart_type == "Candlestick" and all(col in df.columns for col in ["Open", "High", "Low", "Close"]):
                price_traces.append(
                    go.Candlestick(
                        x=df.index,
                        open=df["Open"],
                        high=df["High"],
                        low=df["Low"],
                        close=df["Close"],
                        name=ticker,
                        increasing_line_color=color,
                        decreasing_line_color=color,
                    )
                )
            else:
                price_traces.append(
                    go.Scatter(
                        x=df.index,
                        y=df["Close"],
                        mode="lines",
                        name=ticker,
                        line=dict(color=color, width=2),
                    )
                )

            volume_traces.append(
                go.Bar(
                    x=df.index,
                    y=df["Volume"],
                    name=ticker,
                    marker_color=color,
                    opacity=0.7,
                )
            )

        price_fig = go.Figure(price_traces)
        price_fig.update_layout(
            title="Closing Prices",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template="plotly_white",
            height=450,
        )
        st.plotly_chart(price_fig, width="stretch")

        vol_fig = go.Figure(volume_traces)
        vol_fig.update_layout(
            title="Trading Volume",
            barmode="overlay",
            xaxis_title="Date",
            yaxis_title="Volume",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template="plotly_white",
            height=300,
        )
        st.plotly_chart(vol_fig, width="stretch")

        st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    else:
        st.info("No data available for the selected tickers and date range.")
else:
    st.info("Please select at least one company to view stock data.")
