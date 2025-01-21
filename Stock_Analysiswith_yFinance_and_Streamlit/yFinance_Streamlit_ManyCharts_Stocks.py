import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import time

def create_line_chart(ax, data):
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.set_title('Line Chart')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()

def create_bar_chart(ax, data):
    ax.bar(data.index, data['Volume'], label='Volume')
    ax.set_title('Bar Chart')
    ax.set_xlabel('Date')
    ax.set_ylabel('Volume')
    ax.legend()
    
def create_candlestick_chart(ax, data):
    candlestick_data = data[['Open', 'High', 'Low', 'Close']]
    ax.plot(candlestick_data.index, candlestick_data['Close'], label='Close Price')
    ax.fill_between(candlestick_data.index, candlestick_data['Low'], candlestick_data['High'], color='gray', alpha=0.3)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('Candlestick Chart')
    ax.legend()
    
def create_moving_average_chart(ax, data, window=20):
    data['Moving Average'] = data['Close'].rolling(window=window).mean()
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.plot(data.index, data['Moving Average'], label=f'{window}-Day Moving Average')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('Moving Average Chart')
    ax.legend()

def create_scatter_plot(ax, data):
    ax.scatter(data.index, data['Close'], label='Close Price', alpha=0.5)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('Scatter Plot')
    ax.legend()

def create_histogram(ax, data):
    ax.hist(data['Close'], bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Histogram')
    ax.set_xlabel('Price')
    ax.set_ylabel('Frequency')
    
def create_box_plot(ax, data):
    sns.boxplot(data=data[['Open', 'High', 'Low', 'Close']], ax=ax)
    ax.set_title('Box Plot')
    ax.set_ylabel('Price')
    
def create_density_plot(ax, data):
    sns.kdeplot(data['Close'], ax=ax, shade=True)
    ax.set_xlabel('Price')
    ax.set_title('Density Plot')
    
def create_correlation_heatmap(ax, data):
    corr = data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Heatmap')


# Get stock data
st.set_page_config(page_title="Stock Analysis by Duy Nguyen", layout="wide")

# Sidebar
st.sidebar.title("Stock Analysis by Duy Nguyen")
st.sidebar.markdown("""
## About
This app provides real-time analysis of selected stock prices using various types of charts. 
The data is fetched every minute to keep the information up-to-date.
""")

# Get stock data
st.title('Stock Analysis')
st.markdown("""
### Overview
This application displays various charts to analyze the stock prices of selected companies. 
The charts include line charts, bar charts, candlestick charts, moving averages, scatter plots, box plots, density plots, and correlation heatmaps.
""")

# Fetch stock data
stock_options = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
select_stocks = st.sidebar.selectbox('Select a stock ticker:', stock_options)
stock_data = yf.Ticker(select_stocks)
historical_prices = stock_data.history(period='1d', interval='1m')

# Display charts
fig, axes = plt.subplots(3, 3, figsize=(20, 15))
create_line_chart(axes[0, 0], historical_prices)
create_bar_chart(axes[0, 1], historical_prices)
create_candlestick_chart(axes[0, 2], historical_prices)
create_moving_average_chart(axes[1, 0], historical_prices)
create_scatter_plot(axes[1, 1], historical_prices)
create_histogram(axes[1, 2], historical_prices)
create_box_plot(axes[2, 0], historical_prices)
create_density_plot(axes[2, 1], historical_prices)
create_correlation_heatmap(axes[2, 2], historical_prices)

fig.tight_layout()
st.pyplot(fig)

latest_price = historical_prices['Close'].iloc[-1]
latest_time = historical_prices.index[-1].strftime(format='%Y-%m-%d %H:%M:%S')
st.write(f"### Latest Price ({latest_time}): ${latest_price:.2f}")
st.write('Data is updated every minute. Please refresh the page to get the latest information.')
time.sleep(60)