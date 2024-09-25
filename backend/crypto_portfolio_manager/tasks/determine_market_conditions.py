import pandas as pd
import talib
from tasks.task_base import BaseTask
from utils.indicators import (
    calculate_ichimoku, calculate_trend_strength, calculate_rsi,
    calculate_atr, add_token_metrics_indicators
)

class DetermineMarketConditionsTask(BaseTask):
    def __init__(self):
        super().__init__()

    def execute(self, data: pd.DataFrame):
        data = add_token_metrics_indicators(data)
        trend_strength = calculate_trend_strength(data)
        volatility = data['close'].pct_change().std()
        volume = data['volume'].mean()
        rsi = calculate_rsi(data).iloc[-1]
        atr = calculate_atr(data).iloc[-1]
        sma_50 = talib.SMA(data['close'], timeperiod=50).iloc[-1]
        sma_200 = talib.SMA(data['close'], timeperiod=200).iloc[-1]
        macd, macd_signal, macd_hist = talib.MACD(data['close'])
        ichimoku = calculate_ichimoku(data)
        tm_grade = data['tm_grade'].iloc[-1] if 'tm_grade' in data.columns else None
        tm_trend = data['tm_trend'].iloc[-1] if 'tm_trend' in data.columns else None
        tm_sentiment = data['tm_sentiment'].iloc[-1] if 'tm_sentiment' in data.columns else None
        tm_technical_score = data['tm_technical_score'].iloc[-1] if 'tm_technical_score' in data.columns else None
        return {
            "trend_strength": trend_strength,
            "volatility": volatility,
            "volume": volume,
            "rsi": rsi,
            "atr": atr,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "macd": macd.iloc[-1],
            "macd_signal": macd_signal.iloc[-1],
            "macd_hist": macd_hist.iloc[-1],
            "ichimoku": ichimoku,
            "tm_grade": tm_grade,
            "tm_trend": tm_trend,
            "tm_sentiment": tm_sentiment,
            "tm_technical_score": tm_technical_score
        }
