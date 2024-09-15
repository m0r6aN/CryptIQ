from strategies.base_strategy import BaseStrategy
from data.data_fetcher import DataFetcher
import pandas as pd

class CorrelationStrategy(BaseStrategy):
    def __init__(self, symbol_to_correlate='ETH/USDT', window=20, exchange=None, symbol="BTC/USDT"):
        super().__init__()
        self.symbol_to_correlate = symbol_to_correlate
        self.data_fetcher = DataFetcher()
        self.window = window
        self.exchange = exchange  # Pass the exchange instance (e.g., Binance)
        self.symbol = symbol

    def on_data(self, data):
        # Fetch correlation asset data
        other_data = self.data_fetcher.fetch_data(symbol=self.symbol_to_correlate)
        
        # Merge both datasets on 'datetime' and compute correlation
        merged_data = pd.merge(data[['datetime', 'close']], other_data[['datetime', 'close']], on='datetime', suffixes=('_self', '_other'))
        correlation = merged_data['close_self'].pct_change().rolling(window=self.window).corr(merged_data['close_other'].pct_change()).iloc[-1]

        # Trading signals based on correlation
        if correlation > 0.8 and self.position is None:
            self.enter_position('long', leverage=50)
        elif correlation < -0.8 and self.position is None:
            self.enter_position('short', leverage=50)
        elif self.position is not None:
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
