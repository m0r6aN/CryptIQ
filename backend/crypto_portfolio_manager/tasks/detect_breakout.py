import pandas as pd
from tasks.task_base import BaseTask
from utils.indicators import identify_support_levels, identify_resistance_levels

class DetectBreakoutTask(BaseTask):
    def __init__(self):
        super().__init__()

    def execute(self, data: pd.DataFrame) -> bool:
        support_levels = identify_support_levels(data)
        resistance_levels = identify_resistance_levels(data)
        price = data['close'].iloc[-1]
        return price > resistance_levels[-1] or price < support_levels[-1]
