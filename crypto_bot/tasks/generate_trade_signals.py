from typing import Tuple, List
import pandas as pd
from tasks.task_base import BaseTask

class GenerateTradeSignalsTask(BaseTask):
    def __init__(self, risk_per_trade: float = 0.02):
        super().__init__()
        self.risk_per_trade = risk_per_trade

    def execute(self, data: pd.DataFrame) -> Tuple[List[int], List[float], List[float]]:
        signals = []
        confidences = []
        position_sizes = []

        for i in range(len(data)):
            position = data['position'].iloc[i]
            if position == 1:
                signals.append(1)
                confidences.append(1.0)
            elif position == -1:
                signals.append(-1)
                confidences.append(1.0)
            else:
                signals.append(0)
                confidences.append(0.0)

            if signals[-1] != 0:
                price = data['close'].iloc[i]
                volatility = data['volatility'].iloc[i]
                position_size = (self.risk_per_trade / volatility) * price
                position_sizes.append(position_size)
            else:
                position_sizes.append(0.0)

        return signals, confidences, position_sizes
