from typing import Dict, List, Tuple
import pandas as pd
from tasks.task_base import BaseTask
from utils.indicators import add_indicators, add_token_metrics_indicators

class RankCryptocurrenciesTask(BaseTask):
    def __init__(self):
        super().__init__()

    def execute(self, data_dict: Dict[str, pd.DataFrame]) -> List[Tuple[str, float]]:
        rankings = {}
        for ticker, data in data_dict.items():
            data = add_indicators(data)
            data = add_token_metrics_indicators(data)
            momentum = data['SMA_50'].iloc[-1] / data['SMA_200'].iloc[-1]
            volatility = data['close'].pct_change().std()
            volume = data['volume'].iloc[-1]
            rsi = data['RSI'].iloc[-1]
            tm_grade = data['tm_grade'].iloc[-1] if 'tm_grade' in data.columns else 0
            tm_technical_score = data['tm_technical_score'].iloc[-1] if 'tm_technical_score' in data.columns else 0

            ranking_score = (
                0.3 * momentum +
                0.2 * (1 / volatility) +
                0.2 * volume +
                0.1 * (50 - abs(rsi - 50)) / 50 +
                0.1 * tm_grade +
                0.1 * tm_technical_score
            )
            rankings[ticker] = ranking_score

        return sorted(rankings.items(), key=lambda x: x[1], reverse=True)
