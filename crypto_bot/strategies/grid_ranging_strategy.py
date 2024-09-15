from strategies.base_strategy import BaseStrategy
from utils.indicators import calculate_support_resistance

class GridRangingStrategy(BaseStrategy):
    def __init__(self, grid_levels=5, exchange=None, symbol="BTC/USDT"):
        super().__init__()
        self.grid_levels = grid_levels
        self.grid = []
        self.exchange = exchange  # Pass the exchange instance (e.g., Binance)
        self.symbol = symbol

    def on_data(self, data):
        if not self.grid:
            self.grid = self.create_grid(data)

        price = data['close'].iloc[-1]
        for level in self.grid:
            if price <= level and self.position is None:
                self.enter_position('long', leverage=50)
            elif price >= level and self.position == 'long':
                self.exit_position()

    def create_grid(self, data):
        support, resistance = calculate_support_resistance(data)
        grid_spacing = (resistance - support) / self.grid_levels
        return [support + i * grid_spacing for i in range(1, self.grid_levels)]

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
