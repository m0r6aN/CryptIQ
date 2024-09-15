from .base_strategy import BaseStrategy

class LeverageStrategy(BaseStrategy):
    def should_enter_trade(self, price_data):
        # Set leverage to 50 when entering a trade
        self.trade_executor.set_leverage(50)
        # Implement logic for entering a trade based on price_data
        # Return True if conditions to enter the trade are met
        return True

    def should_exit_trade(self, price_data):
        # Set leverage to 1 when exiting a trade
        self.trade_executor.set_leverage(1)
        # Implement logic for exiting a trade based on price_data
        # Return True if conditions to exit the trade are met
        return True
