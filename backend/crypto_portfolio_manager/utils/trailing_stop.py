# CryptIQ/crypto_bot/utils/trailing_stop.py
def calculate_trailing_stop(price, stop_loss_percentage):
    return price * (1 - stop_loss_percentage)