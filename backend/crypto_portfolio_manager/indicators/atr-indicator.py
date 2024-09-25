# CryptIQ/crypto_bot/indicators/atr_indicator.py
from crypto_bot.utils.indicators import calculate_atr


class ATRIndicator():
    def __init__(self, atr_period=14, atr_multiplier=3, exchange=None, symbol="BTC/USDT"):
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier
        self.exchange = exchange
        self.symbol = symbol
        self.atr = None
        self.entry_price = None
        self.position = None

    def on_data(self, data):
        self.atr = calculate_atr(data, self.atr_period)
        if self.position is None:
            if self.detect_entry_signal(data):
               return "Long"
        else:
            if self.detect_exit_signal(data):
                return "Short"
        return "Hold"

    def detect_entry_signal(self, data):
        # Entry signal based on ATR breakout
        return data['close'].iloc[-1] > data['high'].rolling(window=self.atr_period).max().iloc[-1]

    def detect_exit_signal(self, data):
        # Exit signal based on stop-loss using ATR
        stop_loss = self.entry_price - self.atr_multiplier * self.atr
        return data['close'].iloc[-1] < stop_loss