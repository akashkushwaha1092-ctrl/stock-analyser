import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple Stock Price App

Shown are the stock closing price and volume of Google!
""")

tickerSymbol = 'GOOGL'

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(
    
    start='2025-05-31',
    end='2026-05-31'
)

st.line_chart(tickerDf.Close)

st.line_chart(tickerDf.Volume)