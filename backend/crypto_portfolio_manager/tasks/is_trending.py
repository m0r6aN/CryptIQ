import pandas as pd
from tasks.task_base import BaseTask

class IsTrendingTask(BaseTask):
    def __init__(self, short_period: int = 20, long_period: int = 50):
        super().__init__()
        self.short_period = short_period
        self.long_period = long_period

    def execute(self, data: pd.DataFrame) -> bool:
        sma_short = data['close'].rolling(window=self.short_period).mean()
        sma_long = data['close'].rolling(window=self.long_period).mean()
        return sma_short.iloc[-1] > sma_long.iloc[-1] or sma_short.iloc[-1] < sma_long.iloc[-1]
