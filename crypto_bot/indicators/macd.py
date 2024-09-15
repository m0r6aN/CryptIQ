import numpy as np

def calculate_macd(price_data, short_window=12, long_window=26, signal_window=9):
    short_ma = np.mean(price_data[-short_window:])
    long_ma = np.mean(price_data[-long_window:])
    macd = short_ma - long_ma
    signal = np.mean(price_data[-signal_window:])
    return macd, signal
