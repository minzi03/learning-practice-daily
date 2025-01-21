# =============================================================================
# Real-time Apple Stock Prices Visualization using yfinance and Streamlit
# =============================================================================

import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time

# Define the ticker symbol for Apple
ticker_symbol = 'AAPL'

# Get the stock data for Apple
apple_stock = yf.Ticker(ticker_symbol)

# Create a matplotlib figure
fig, ax = plt.subplots()

# Use st.pyplot to display the plot in the Streamlit app
plot = st.pylot(fig)

# Loop to get and update the stock price
while True:
    # Get the historical prices of Apple stock
    historical_prices = apple_stock.history(period='1d', interval='1m')
    
    # Get the latest price and time
    lastest_price = historical_prices['Close'].iloc[-1]
    latest_time = historical_prices.index[-1].strftime('%H:%M:%S')
    
    # Clear the old plot and plot on the new data
    ax.clear()
    ax.plot(historical_prices.index, historical_prices['Close'], label='Stock Value')
    ax.set_xlabel('Time')
    ax.set_ylabel('Stock Value')
    ax.set_title('Apple Stock Value by Duy Nguyen')
    ax.legend(loc='upper left')
    ax.tick_params(axis='x', rotation=45)
    
    # Update the plot in the Streamlit app
    plot.pyplot(fig)
    
    # Display the latest stock price in the app
    st.write(f"Latest Price ({latest_time}): {latest_price}")
    
    # Pause for 1 minute before getting new data
    time.sleep(60)