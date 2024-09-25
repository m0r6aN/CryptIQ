# This BaseStrategy class provides a foundation for strategies with trade_executor, risk_manager, and a reusable method calculate_position_size. 
# It allows other strategy classes to inherit and implement their own on_data, should_enter_trade, and should_exit_trade methods.
# Consider expanding the BaseStrategy class with additional methods or properties that can be shared across multiple strategies.

class BaseStrategy:
    def __init__(self, trade_executor, risk_manager, exchange=None):
        self.trade_executor = trade_executor
        self.risk_manager = risk_manager
        self.exchange = exchange

    def on_data(self, data):
        raise NotImplementedError("Must implement on_data method")

    def should_enter_trade(self):
        raise NotImplementedError

    def should_exit_trade(self):
        raise NotImplementedError

    def calculate_position_size(self, price, account_balance, risk_per_trade=0.02, leverage=1):
        risk_amount = account_balance * risk_per_trade
        position_size = (risk_amount / price) * leverage
        return min(position_size, account_balance / price)