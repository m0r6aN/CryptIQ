import pandas as pd
import talib
import numpy as np

def calculate_fibonacci_levels(data):
    high = data['high'].max()
    low = data['low'].min()

    # Calculate Fibonacci levels
    diff = high - low
    fib_levels = {
        'level_0': high,
        'level_23.6': high - 0.236 * diff,
        'level_38.2': high - 0.382 * diff,
        'level_50': high - 0.5 * diff,
        'level_61.8': high - 0.618 * diff,
        'level_100': low
    }
    return fib_levels

def calculate_fib_stop_loss(entry_price, fib_levels, position_type):
    if position_type == 'Long':
        return fib_levels['level_61.8']  # Stop-loss below the 61.8% retracement
    elif position_type == 'Short':
        return fib_levels['level_38.2']  # Stop-loss above the 38.2% retracement
    return None

def calculate_fib_take_profits(entry_price, fib_levels, position_type):
    if position_type == 'Long':
        return [fib_levels['level_23.6'], fib_levels['level_38.2'], fib_levels['level_50']]  # Laddering take-profits
    elif position_type == 'Short':
        return [fib_levels['level_50'], fib_levels['level_38.2'], fib_levels['level_23.6']]
    return []

def calculate_leverage(adx_value, atr_value, trend_strength):
    if adx_value < 25:
        return 2  # Weak trend, no leverage
    elif adx_value < 50 and atr_value < 0.02 and trend_strength > 0.5:
        return 5  # Moderate trend, small leverage
    elif adx_value < 75 and atr_value < 0.04 and trend_strength > 0.7:
        return 10  # Strong trend, medium leverage
    elif adx_value >= 75 and atr_value < 0.06 and trend_strength > 0.85:
        return 20 # Very strong trend, higher leverage
    else:
        return 1  # Default to no leverage if conditions aren't favorable

def compound_profit(current_balance, profit_percentage):
    return current_balance * (1 + profit_percentage)

def calculate_trend_strength(data):
    roc = data['close'].pct_change()
    ema = talib.EMA(roc, timeperiod=14)
    return ema.iloc[-1]

def calculate_rsi(data: pd.DataFrame, period=14):
    return talib.RSI(data['close'], timeperiod=period)

def calculate_ichimoku(data):
    high9 = data['high'].rolling(window=9).max()
    low9 = data['low'].rolling(window=9).min()
    tenkan_sen = (high9 + low9) / 2

    high26 = data['high'].rolling(window=26).max()
    low26 = data['low'].rolling(window=26).min()
    kijun_sen = (high26 + low26) / 2

    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    high52 = data['high'].rolling(window=52).max()
    low52 = data['low'].rolling(window=52).min()
    senkou_span_b = ((high52 + low52) / 2).shift(26)

    chikou_span = data['close'].shift(-26)

    ichimoku = pd.DataFrame({
        'tenkan_sen': tenkan_sen,
        'kijun_sen': kijun_sen,
        'senkou_span_a': senkou_span_a,
        'senkou_span_b': senkou_span_b,
        'chikou_span': chikou_span
    })
    return ichimoku

def calculate_token_metrics_indicator(data: pd.DataFrame, indicator_name: str):
    if indicator_name in data.columns:
        return data[indicator_name]
    else:
        return pd.Series([None]*len(data))
    
def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(period).mean()
    return atr

def calculate_atr_trailing_stop(self, df: pd.DataFrame, atr: float) -> float:
    src = df['close'] if not self.h else df['close']  # We don't have Heikin Ashi in this implementation
    n_loss = self.a * atr
    atr_trailing_stop = src.iloc[-1] - n_loss if src.iloc[-1] > src.iloc[-2] else src.iloc[-1] + n_loss
    return atr_trailing_stop

def calculate_position_size(self, symbol: str) -> float:
    balance = self.exchange.fetch_balance()
    equity = balance['total']['USDT']
    current_price = self.exchange.fetch_ticker(symbol)['last']
    return (equity * self.leverage) / current_price

def calculate_stop_loss(df, position_type):
    if position_type == 'Long':
        return df['low'].rolling(window=14).min().iloc[-1]
    elif position_type == 'Short':
        return df['high'].rolling(window=14).max().iloc[-1]

def calculate_take_profit(df, position_type):
    if position_type == 'Long':
        return df['high'].rolling(window=14).max().iloc[-1]
    elif position_type == 'Short':
        return df['low'].rolling(window=14).min().iloc[-1]