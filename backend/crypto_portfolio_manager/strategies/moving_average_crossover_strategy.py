from strategies.base_strategy import BaseStrategy
from utils.indicators import MovingAverage

class MovingAverageCrossoverStrategy(BaseStrategy):
    def __init__(self, fast_window=50, slow_window=200):
        super().__init__()
        self.ma_fast = MovingAverage(window=fast_window)
        self.ma_slow = MovingAverage(window=slow_window)

    def on_data(self, data):
        ma_fast_value = self.ma_fast.calculate(data['close'])
        ma_slow_value = self.ma_slow.calculate(data['close'])

        if ma_fast_value > ma_slow_value and self.position is None:
            self.enter_position('long', leverage=50)
        elif ma_fast_value < ma_slow_value and self.position == 'long':
            self.exit_position()
        elif ma_fast_value < ma_slow_value and self.position is None:
            self.enter_position('short', leverage=50)
        elif ma_fast_value > ma_slow_value and self.position == 'short':
            self.exit_position()
    
    def enter_position(self, side, leverage):
        self.position = side
        self.entry_price = self.data['close'].iloc[-1]
        print(f"Entered {side} position at price: {self.entry_price} with {leverage}x leverage")

    def exit_position(self):
        exit_price = self.data['close'].iloc[-1]
        if self.position == 'long':
            profit = (exit_price - self.entry_price) * 50  # Leverage is fixed at 50
        elif self.position == 'short':
            profit = (self.entry_price - exit_price) * 50

        self.current_balance += profit
        print(f"Exited {self.position} position at price: {exit_price}. Profit: {profit}")
        self.position = None
        self.entry_price = None
