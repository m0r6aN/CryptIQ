from strategies.base_strategy import BaseStrategy
from utils.indicators import calculate_ichimoku

class IchimokuCloudStrategy(BaseStrategy):
    def __init__(self, exchange=None, symbol="BTC/USDT"):
        super().__init__()
        self.exchange = exchange  # Pass the exchange instance (e.g., Binance)
        self.symbol = symbol

    def on_data(self, data):
        ichimoku = calculate_ichimoku(data)
        tenkan_sen = ichimoku['tenkan_sen'].iloc[-1]
        kijun_sen = ichimoku['kijun_sen'].iloc[-1]
        senkou_span_a = ichimoku['senkou_span_a'].iloc[-1]
        senkou_span_b = ichimoku['senkou_span_b'].iloc[-1]
        price = data['close'].iloc[-1]

        if tenkan_sen > kijun_sen and price > senkou_span_a and price > senkou_span_b and self.position is None:
            self.enter_position('long', leverage=50)
        elif tenkan_sen < kijun_sen and price < senkou_span_a and price < senkou_span_b and self.position is None:
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
