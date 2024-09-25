# CryptIQ/crypto_bot/indicators/breakout-finder.py
from utils.indicators import identify_support_levels, identify_resistance_levels

class BreakoutIndicator():
    def __init__(self, data):
        super().__init__()
        self.exchange = exchange  # Pass the exchange instance (e.g., Binance)
        self.symbol = symbol

    def on_data(self, data):
        support_levels = identify_support_levels(data)
        resistance_levels = identify_resistance_levels(data)
        price = data['close'].iloc[-1]

        if price > resistance_levels[-1] and self.position is None:
            self.enter_position('long', leverage=50)
        elif price < support_levels[-1] and self.position is None:
            self.enter_position('short', leverage=50)
        elif self.position is not None:
            self.exit_position()