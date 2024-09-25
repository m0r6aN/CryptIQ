# CryptIQ/crypto_bot/indicators/momentum_indicator.py
from crypto_bot.indicators.rsi import calculate_rsi

class MomentumIndicator():
    def __init__(self, exchange=None, symbol="BTC/USDT"):
        self.rsi_overbought = 70
        self.rsi_oversold = 30
        self.exchange = exchange
        self.symbol = symbol
        self.position = None

    def on_data(self, data):
        rsi = calculate_rsi(data).iloc[-1]
        if rsi > self.rsi_overbought and self.position != 'Short':
            self.position = 'Short'
            return "Short"
        elif rsi < self.rsi_oversold and self.position != 'Long':
            self.position = 'Long'
            return "Long"
        else:
            return "Hold"