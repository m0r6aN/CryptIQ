# This BaseStrategy class provides a foundation for strategies with trade_executor, risk_manager, and a reusable method calculate_position_size. 
# It allows other strategy classes to inherit and implement their own on_data, should_enter_trade, and should_exit_trade methods.
# Consider expanding the BaseStrategy class with additional methods or properties that can be shared across multiple strategies.

class BaseStrategy:
    def __init__(self, trade_executor, risk_manager, exchange=None):
        self.trade_executor = trade_executor
        self.risk_manager = risk_manager
        self.exchange = exchange  # Exchange instance (e.g., Binance)

    def on_data(self, data):
        raise NotImplementedError("Must implement on_data method")

    def should_enter_trade(self):
        raise NotImplementedError

    def should_exit_trade(self):
        raise NotImplementedError
    
    def calculate_position_size(self, price, leverage):
        # Fetch the balance from the exchange
        balance = self.exchange.fetch_balance()
        usdt_balance = balance['free']['USDT']
        
        # Define risk percentage (e.g., 2% of the balance)
        risk_percentage = 0.02
        risk_capital = usdt_balance * risk_percentage  # Amount willing to risk

        # Calculate position size based on risk, price, and leverage
        position_size = (risk_capital / price) * leverage
        
        # Ensure position size does not exceed available balance
        if position_size * price > usdt_balance:
            position_size = usdt_balance / price

        return position_size
