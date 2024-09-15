from strategies.base_strategy import BaseStrategy
from utils.indicators import calculate_atr

class ATRStrategy(BaseStrategy):
    def __init__(self, atr_period=14, atr_multiplier=3, exchange=None, symbol="BTC/USDT"):
        super().__init__()
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier
        self.exchange = exchange  # Pass the exchange instance (e.g., Binance)
        self.symbol = symbol
        self.atr = None
        self.entry_price = None

    def on_data(self, data):
        self.atr = calculate_atr(data, self.atr_period)
        if self.position is None:
            if self.detect_entry_signal(data):
                self.enter_position('long', leverage=50)
                self.entry_price = data['close'].iloc[-1]
        else:
            if self.detect_exit_signal(data):
                self.exit_position()

    def detect_entry_signal(self, data):
        # Entry signal based on ATR breakout
        return data['close'].iloc[-1] > data['high'].rolling(window=self.atr_period).max().iloc[-1]

    def detect_exit_signal(self, data):
        # Exit signal based on stop-loss using ATR
        stop_loss = self.entry_price - self.atr_multiplier * self.atr
        return data['close'].iloc[-1] < stop_loss

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
