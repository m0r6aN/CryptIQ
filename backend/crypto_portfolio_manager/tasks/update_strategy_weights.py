from typing import Dict
from tasks.task_base import BaseTask

class UpdateStrategyWeightsTask(BaseTask):
    def __init__(self, strategy_weights: Dict[str, float]):
        super().__init__()
        self.strategy_weights = strategy_weights

    def execute(self, market_conditions: Dict[str, float]) -> Dict[str, float]:
        ranging_market = (1 - market_conditions["trend_strength"]) * 0.5 + \
                         (1 - market_conditions["volatility"]) * 0.3 + \
                         (1 - abs(market_conditions["rsi"] - 50) / 50) * 0.2

        tm_trend = market_conditions.get("tm_trend", 0)
        tm_sentiment = market_conditions.get("tm_sentiment", 0)
        tm_grade = market_conditions.get("tm_grade", 0)
        tm_technical_score = market_conditions.get("tm_technical_score", 0)

        self.strategy_weights["grid_ranging_strategy"] = ranging_market * 0.8 + \
                                                         (1 - market_conditions["volatility"]) * 0.1 + \
                                                         (1 - tm_trend) * 0.1

        self.strategy_weights["turtle_trending_strategy"] = market_conditions["trend_strength"] * 0.7 + \
                                                            tm_trend * 0.2 + \
                                                            tm_grade * 0.1

        self.strategy_weights["atr_strategy"] = market_conditions["atr"] * 0.6 + \
                                                market_conditions["volatility"] * 0.2 + \
                                                tm_technical_score * 0.2

        self.strategy_weights["rsi_divergence_strategy"] = abs(market_conditions["rsi"] - 50) / 50 * 0.6 + \
                                                           market_conditions["volatility"] * 0.2 + \
                                                           tm_sentiment * 0.2

        # Update other strategies similarly, incorporating Token Metrics data
        return self.strategy_weights
