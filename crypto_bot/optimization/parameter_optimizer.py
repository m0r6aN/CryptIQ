from backtesting.backtester import Backtester
from strategies.moving_average_crossover_strategy import MovingAverageCrossoverStrategy
import pandas as pd

class ParameterOptimizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def optimize(self):
        best_performance = -float('inf')
        best_params = None

        for fast_window in range(5, 50, 5):
            for slow_window in range(60, 200, 10):
                strategy = MovingAverageCrossoverStrategy(fast_window=fast_window, slow_window=slow_window)
                backtester = Backtester(strategy, self.data)
                backtester.run()
                performance = self.calculate_performance(backtester)
                if performance > best_performance:
                    best_performance = performance
                    best_params = (fast_window, slow_window)

        return best_params

    def calculate_performance(self, backtester: Backtester):
        # Simple performance metric: final balance
        return backtester.current_balance - backtester.initial_balance
