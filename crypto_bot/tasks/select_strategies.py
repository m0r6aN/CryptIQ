from typing import List, Dict
import pandas as pd
from tasks.task_base import BaseTask

class SelectStrategiesTask(BaseTask):
    def __init__(self, strategy_weights: Dict[str, float], top_n: int = 3):
        super().__init__(name="SelectStrategies", description="Selects the top N strategies based on the updated strategy weights.")
        self.strategy_weights = strategy_weights
        self.top_n = top_n

    def execute(self, data: pd.DataFrame) -> List[str]:
        # Assume that DetermineMarketConditionsTask and UpdateStrategyWeightsTask are initialized
        market_conditions = self.determine_market_conditions_task.execute(data)
        updated_weights = self.update_strategy_weights_task.execute(market_conditions)

        # Sort strategies based on their weights
        sorted_strategies = sorted(updated_weights.items(), key=lambda x: x[1], reverse=True)

        # Select top N strategies
        return [strategy for strategy, _ in sorted_strategies[:self.top_n]]
