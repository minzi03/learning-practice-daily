# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 16:31:41 2024

@author: X1 Carbon Gen 7
"""

import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import time

ticker_symbol = 'AAPL'
apple_stock = yf.Ticker(ticker_symbol)

def create_line_chart(ax, data):
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title('Line Chart')
    ax.legend()

def create_bar_chart(ax, data):
    ax.bar(data.index, data['Volume'], label='Volume')
    ax.set_xlabel('Time')
    ax.set_ylabel('Volume')
    ax.set_title('Bar Chart')
    ax.legend()

def create_candlestick_chart(ax, data):
    candlestick_data = data[['Open', 'High', 'Low', 'Close']]
    ax.plot(candlestick_data.index, candlestick_data['Close'], label='Close Price')
    ax.fill_between(candlestick_data.index, candlestick_data['Low'], candlestick_data['High'], color='gray', alpha=0.3)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title('Candlestick Chart')
    ax.legend()

def create_moving_average_chart(ax, data, window=20):
    data['Moving Average'] = data['Close'].rolling(window=window).mean()
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.plot(data.index, data['Moving Average'], label=f'{window}-Day Moving Average')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title('Moving Average Chart')
    ax.legend()

def create_scatter_plot(ax, data):
    ax.scatter(data.index, data['Close'], label='Close Price', alpha=0.5)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title('Scatter Plot')
    ax.legend()

def create_box_plot(ax, data):
    sns.boxplot(data=data[['Open', 'High', 'Low', 'Close']], ax=ax)
    ax.set_title('Box Plot')

def create_density_plot(ax, data):
    sns.kdeplot(data['Close'], ax=ax, shade=True)
    ax.set_xlabel('Price')
    ax.set_title('Density Plot')

def create_correlation_heatmap(ax, data):
    corr = data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Heatmap')

st.set_page_config(page_title="Apple Stock Analysis", layout="wide")

st.sidebar.title("Apple Stock Analysis by Duy Nguyen")
st.sidebar.markdown("""
## About
This app provides real-time analysis of Apple (AAPL) stock prices using various types of charts. 
The data is fetched every minute to keep the information up-to-date.
""")

st.title('Apple Stock Analysis by Duy Nguyen')
st.markdown("""
### Overview
This application displays various charts to analyze the stock prices of Apple Inc. (AAPL). 
The charts include line charts, bar charts, candlestick charts, moving averages, scatter plots, box plots, density plots, and correlation heatmaps.
""")

while True:
    historical_prices = apple_stock.history(period='1d', interval='1m')
    
    fig, axs = plt.subplots(3, 3, figsize=(20, 15))
    
    create_line_chart(axs[0, 0], historical_prices)
    create_bar_chart(axs[0, 1], historical_prices)
    create_candlestick_chart(axs[0, 2], historical_prices)
    create_moving_average_chart(axs[1, 0], historical_prices)
    create_scatter_plot(axs[1, 1], historical_prices)
    create_box_plot(axs[1, 2], historical_prices)
    create_density_plot(axs[2, 0], historical_prices)
    create_correlation_heatmap(axs[2, 1], historical_prices)
    
    fig.tight_layout()
    st.pyplot(fig)
    
    latest_price = historical_prices['Close'].iloc[-1]
    latest_time = historical_prices.index[-1].strftime('%H:%M:%S')
    
    st.write(f"### Latest Price ({latest_time}): ${latest_price:.2f}")
    
    time.sleep(60)