import numpy as np

def get_moving_average(price_data, window):
    return np.mean(price_data[-window:])
