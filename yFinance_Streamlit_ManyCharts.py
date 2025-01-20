import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Define the ticker symbol
ticker_symbol = 'AAPL'

# Fetch the data
apple_stock = yf.Ticker(ticker_symbol)

def create_line_chart(ax, data):
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.set_title(f'{ticker_symbol} Line Chart')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    
def create_bar_chart(ax, data):
    ax.bar(data.index, data['Volume'], label='Volume')
    ax.set_title(f'{ticker_symbol} Bar Chart')
    ax.set_xlabel('Date')
    ax.set_ylabel('Volume')
    ax.legend()
    
def create_candlestick_chart(ax, data):
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.set_title(f'{ticker_symbol} Candlestick Chart')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    
    ax2 = ax.twinx()
    ax2.bar(data.index, data['Volume'], label='Volume', alpha=0.3)
    ax2.set_ylabel('Volume')
    ax2.legend(loc='upper right')
    
def create_heatmap(ax, data):
    sns.heatmap(data.corr(), annot=True, ax=ax)
    ax.set_title(f'{ticker_symbol} Correlation Heatmap')
    
def create_moving_average_chart(ax, data, window=20):
    data['Moving Average'] = data['Close'].rolling(window=window).mean()
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.plot(data.index, data['Moving Average'], label=f'{window} Day Moving Average')
    ax.set_title(f'{ticker_symbol} Moving Average Chart')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    
def create_scatter_plot(ax, data):
    ax.scatter(data['Close'], data['Volume'])
    ax.set_title(f'{ticker_symbol} Scatter Plot')
    ax.set_xlabel('Close Price')
    ax.set_ylabel('Volume')
    
def create_box_plot(ax, data):
    sns.boxplot(data=data[['Open', 'High', 'Low', 'Close']], ax=ax)
    ax.set_title(f'{ticker_symbol} Box Plot')
    
def create_desity_plot(ax, data):
    sns.kdeplot(data['Close'], ax=ax)
    ax.set_xlabel('Close Price')
    ax.set_title(f'{ticker_symbol} Desity Plot')
    
def create_correration_plot(ax, data):
    corr = data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title(f'{ticker_symbol} Correlation Heatmap')
    
st.set_page_config(page_title='Apple Stock Analysis', layout='wide')

st.sidebar.title('Apple Stock Analysis by Duy Nguyen')
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
    create_heatmap(axs[1, 0], historical_prices)
    create_moving_average_chart(axs[1, 1], historical_prices)
    create_scatter_plot(axs[1, 2], historical_prices)
    create_box_plot(axs[2, 0], historical_prices)
    create_desity_plot(axs[2, 1], historical_prices)
    create_correration_plot(axs[2, 2], historical_prices)
    
    fig.tight_layout()
    st.pyplot(fig)
    
    lastest_price = historical_prices['Close'].iloc[-1]
    latet_time = historical_prices.index[-1].strftime('format="%Y-%m-%d %H:%M:%S"')
    
    st.write(f'Lastest Close Price: {lastest_price}')
    st.write(f'Lastest Time: {latet_time}')
    
    time.sleep(60)