from strategies.base_strategy import BaseStrategy
from utils.indicators import calculate_rsi

class RSIDivergenceStrategy(BaseStrategy):
    def __init__(self, rsi_period=14, exchange=None, symbol="BTC/USDT"):
        super().__init__()
        self.rsi_period = rsi_period
        self.previous_price = None
        self.previous_rsi = None
        self.exchange = exchange  # Pass the exchange instance (e.g., Binance)
        self.symbol = symbol

    def on_data(self, data):
        current_price = data['close'].iloc[-1]
        current_rsi = calculate_rsi(data, self.rsi_period).iloc[-1]

        if self.previous_price is not None and self.previous_rsi is not None:
            # Bearish divergence: price is higher, RSI is lower
            if (current_price > self.previous_price and current_rsi < self.previous_rsi) and self.position is None:
                self.enter_position('short', leverage=50)
            # Bullish divergence: price is lower, RSI is higher
            elif (current_price < self.previous_price and current_rsi > self.previous_rsi) and self.position is None:
                self.enter_position('long', leverage=50)
            elif self.position is not None:
                self.exit_position()

        self.previous_price = current_price
        self.previous_rsi = current_rsi

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
