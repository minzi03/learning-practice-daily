# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 16:53:50 2024

@author: X1 Carbon Gen 7
"""

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import time

def create_line_chart(data):
    fig = px.line(data, x=data.index, y='Close', title='Line Chart of Close Price')
    return fig

def create_bar_chart(data):
    fig = px.bar(data, x=data.index, y='Volume', title='Bar Chart of Volume')
    return fig

def create_candlestick_chart(data):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(title='Candlestick Chart')
    return fig

def create_moving_average_chart(data, window=20):
    data['Moving Average'] = data['Close'].rolling(window=window).mean()
    fig = px.line(data, x=data.index, y=['Close', 'Moving Average'], title=f'{window}-Day Moving Average Chart')
    return fig

def create_scatter_plot(data):
    fig = px.scatter(data, x=data.index, y='Close', title='Scatter Plot of Close Price')
    return fig

def create_box_plot(data):
    fig = px.box(data, y=['Open', 'High', 'Low', 'Close'], title='Box Plot of Prices')
    return fig

def create_density_plot(data):
    fig = px.density_contour(data, x='Close', title='Density Plot of Close Prices')
    return fig

def create_correlation_heatmap(data):
    corr = data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
    fig = px.imshow(corr, text_auto=True, title='Correlation Heatmap')
    return fig

st.set_page_config(page_title="Stock Analysis", layout="wide")

st.sidebar.title("Stock Analysis by Duy Nguyen")
st.sidebar.markdown("""
## About
This app provides real-time analysis of selected stock prices using various types of charts. 
The data is fetched every minute to keep the information up-to-date.
""")

st.title('Stock Analysis ')
st.markdown("""
### Overview
This application displays various charts to analyze the stock prices of selected companies. 
The charts include line charts, bar charts, candlestick charts, moving averages, scatter plots, box plots, density plots, and correlation heatmaps.
""")

# Danh sách các mã cổ phiếu
stock_options = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
selected_stock = st.sidebar.selectbox('Select a stock ticker:', stock_options)

# Lấy dữ liệu cổ phiếu dựa trên lựa chọn
stock_data = yf.Ticker(selected_stock)
historical_prices = stock_data.history(period='1d', interval='1m')

# Tạo các biểu đồ
line_chart = create_line_chart(historical_prices)
bar_chart = create_bar_chart(historical_prices)
candlestick_chart = create_candlestick_chart(historical_prices)
moving_average_chart = create_moving_average_chart(historical_prices)
scatter_plot = create_scatter_plot(historical_prices)
box_plot = create_box_plot(historical_prices)
density_plot = create_density_plot(historical_prices)
correlation_heatmap = create_correlation_heatmap(historical_prices)

# Hiển thị các biểu đồ
st.plotly_chart(line_chart)
st.plotly_chart(bar_chart)
st.plotly_chart(candlestick_chart)
st.plotly_chart(moving_average_chart)
st.plotly_chart(scatter_plot)
st.plotly_chart(box_plot)
st.plotly_chart(density_plot)
st.plotly_chart(correlation_heatmap)

latest_price = historical_prices['Close'].iloc[-1]
latest_time = historical_prices.index[-1].strftime('%H:%M:%S')

st.write(f"### Latest Price ({latest_time}): ${latest_price:.2f}")