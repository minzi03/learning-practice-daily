# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 11:15:34 2024

@author: X1 Carbon Gen 7
"""

# =============================================================================
# Real-time Apple Stock Prices Visualization using yfinance and Streamlit
# =============================================================================

# pip install streamlit

# Import các thư viện cần thiết    
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time

# Định nghĩa mã cổ phiếu của Apple
ticker_symbol = 'AAPL'

# Lấy dữ liệu cổ phiếu của Apple
apple_stock = yf.Ticker(ticker_symbol)

# Tạo một biểu đồ matplotlib
fig, ax = plt.subplots()

# Sử dụng st.pyplot để hiển thị biểu đồ trong ứng dụng Streamlit
plot = st.pyplot(fig)

# Vòng lặp để lấy và cập nhật giá cổ phiếu
while True:
    # Lấy giá lịch sử của cổ phiếu Apple
    historical_prices = apple_stock.history(period='1d', interval='1m')
    
    # Lấy giá và thời gian mới nhất
    latest_price = historical_prices['Close'].iloc[-1]
    latest_time = historical_prices.index[-1].strftime('%H:%M:%S')
    
    # Xóa biểu đồ cũ và vẽ trên dữ liệu mới
    ax.clear()
    ax.plot(historical_prices.index, historical_prices['Close'], label='Stock Value')
    ax.set_xlabel('Time')
    ax.set_ylabel('Stock Value')
    ax.set_title('Apple Stock Value by Huy Nguyen Quoc')
    ax.legend(loc='upper left')
    ax.tick_params(axis='x', rotation=45)
    
    # Cập nhật biểu đồ trong ứng dụng Streamlit
    plot.pyplot(fig)
    
    # Hiển thị giá cổ phiếu mới nhất trong ứng dụng
    st.write(f"Latest Price ({latest_time}): {latest_price}")
    
    # Dừng 1 phút trước khi lấy dữ liệu mới
    time.sleep(60)

# =============================================================================

# # Running the App - mở terminal của Anaconda và gõ lệnh:
# # Bước 1 - truy cập đến đường dẫn: cd C:\Users\X1 Carbon Gen 7\VTI_PythonLesson09
# # Bước 2 - chạy file: streamlit run yFinance_Streamlit.py
# =============================================================================











