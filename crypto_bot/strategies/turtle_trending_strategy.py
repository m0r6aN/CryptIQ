from strategies.base_strategy import BaseStrategy
import pandas as pd

class TurtleTrendingStrategy(BaseStrategy):
    def __init__(self, entry_period=20, exit_period=10, exchange=None, symbol="BTC/USDT"):
        super().__init__()
        self.entry_period = entry_period
        self.exit_period = exit_period
        self.exchange = exchange  # Pass the exchange instance (e.g., Binance)
        self.symbol = symbol

    def on_data(self, data):
        high_entry = data['high'].rolling(window=self.entry_period).max().iloc[-1]
        low_entry = data['low'].rolling(window=self.entry_period).min().iloc[-1]
        high_exit = data['high'].rolling(window=self.exit_period).max().iloc[-1]
        low_exit = data['low'].rolling(window=self.exit_period).min().iloc[-1]
        price = data['close'].iloc[-1]

        if price >= high_entry and self.position is None:
            self.enter_position('long', leverage=50)
        elif price <= low_entry and self.position is None:
            self.enter_position('short', leverage=50)
        elif self.position == 'long' and price <= low_exit:
            self.exit_position()
        elif self.position == 'short' and price >= high_exit:
            self.exit_position()

    def enter_position(self, side, leverage):
        self.position = side
        self.entry_price = self.data['close'].iloc[-1]
        amount = self.calculate_position_size(self.exchange, self.entry_price, leverage)
        
        if side == 'long':
            order = self.exchange.create_market_buy_order(self.symbol, amount)
        elif side == 'short':
            order = self.exchange.create_market_sell_order(self.symbol, amount)
        
        print(f"Entered {side} position at price: {self.entry_price} with {leverage}x leverage. Order ID: {order['id']}")

    def exit_position(self):
        exit_price = self.data['close'].iloc[-1]
        amount = self.calculate_position_size(self.exchange, self.entry_price, self.leverage)
        
        if self.position == 'long':
            order = self.exchange.create_market_sell_order(self.symbol, amount)
        elif self.position == 'short':
            order = self.exchange.create_market_buy_order(self.symbol, amount)

        print(f"Exited {self.position} position at price: {exit_price}. Order ID: {order['id']}")
        self.position = None
        self.entry_price = None
        self.leverage = None
