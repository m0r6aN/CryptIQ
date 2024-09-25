import numpy as np

def calculate_rsi(price_data, window=14):
    delta = np.diff(price_data)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    avg_gain = np.mean(gain[-window:])
    avg_loss = np.mean(loss[-window:])
    
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
