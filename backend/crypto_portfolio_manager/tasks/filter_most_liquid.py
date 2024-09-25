import pandas as pd
from tasks.task_base import BaseTask

class FilterMostLiquidTask(BaseTask):
    def __init__(self, top_n: int = 10):
        super().__init__()
        self.top_n = top_n

    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        filtered_data = data[data['volume'] > 0]
        filtered_data = filtered_data.sort_values('volume', ascending=False)
        return filtered_data.head(self.top_n)
