import numpy as np

def get_bollinger_bands(price_data, window):
    sma = np.mean(price_data[-window:])
    std = np.std(price_data[-window:])
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    return lower_band, upper_band