import os
import sys
import talib
import logging
from aiohttp import ClientSession

# Configure logging and paths
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from utils.shared import DataFetcher
from utils.calculators import calculate_fib_stop_loss, calculate_fib_take_profits, calculate_fibonacci_levels, calculate_leverage, calculate_stop_loss, calculate_take_profit
from utils.indicators import calculate_atr, calculate_trend_strength

async def analyze_weekly(df):
    # Calculate indicators
    df['SMA_50'] = talib.SMA(df['close'], timeperiod=50)
    df['SMA_200'] = talib.SMA(df['close'], timeperiod=200)
    
    # Determine trend
    if df['SMA_50'].iloc[-1] > df['SMA_200'].iloc[-1]:
        return 'Bullish'
    elif df['SMA_50'].iloc[-1] < df['SMA_200'].iloc[-1]:
        return 'Bearish'
    else:
        return 'Neutral'

async def analyze_daily(df):
    # Calculate indicators
    df['SMA_20'] = talib.SMA(df['close'], timeperiod=20)
    df['SMA_50'] = talib.SMA(df['close'], timeperiod=50)
    
    # Determine signal
    if df['close'].iloc[-1] > df['SMA_20'].iloc[-1] and df['close'].iloc[-1] > df['SMA_50'].iloc[-1]:
        return 'Breakout'
    elif df['close'].iloc[-1] < df['SMA_20'].iloc[-1] and df['close'].iloc[-1] < df['SMA_50'].iloc[-1]:
        return 'Breakdown'
    else:
        return 'Range'

async def analyze_4h(df, symbol):
    # Calculate indicators
    df['SAR'] = talib.SAR(df['high'], df['low'], acceleration=0.02, maximum=0.2)
    df['ADX'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
    df['CCI'] = talib.CCI(df['high'], df['low'], df['close'], timeperiod=20)
    df['volume_ma'] = df['volume'].rolling(window=50).mean()

    # Entry Criteria (Long Position):
    if (df['SAR'].iloc[-1] < df['close'].iloc[-1] and
        df['ADX'].iloc[-1] > 25 and
        df['CCI'].iloc[-1] > -100 and
        df['CCI'].iloc[-2] <= -100 and
        df['volume'].iloc[-1] > df['volume_ma'].iloc[-1]):
        
        entry_price = df['close'].iloc[-1]
        fib_levels = calculate_fibonacci_levels(df)
        tp_levels = calculate_fib_take_profits(entry_price, fib_levels, "Long")
        stop_loss = calculate_fib_stop_loss(entry_price, fib_levels, "Long")
        leverage = calculate_leverage(df['ADX'].iloc[-1], df['ATR'].iloc[-1], calculate_trend_strength(df))
        
        logging.info(f"Long position for {symbol} with leverage {leverage}, Entry at {entry_price}, Take profits at {tp_levels}, Stop-loss at {stop_loss}")
        return {
            'Symbol': symbol,
            'Signal': 'Long',
            'Entry': entry_price,
            'Leverage': leverage,
            'TakeProfits': tp_levels,
            'StopLoss': stop_loss
        }

    # Exit Criteria (Short Position):
    elif (df['SAR'].iloc[-1] > df['close'].iloc[-1] or
          df['ADX'].iloc[-1] < 25 or
          df['CCI'].iloc[-1] < 100 and
          df['CCI'].iloc[-2] >= 100):
        
        exit_price = df['close'].iloc[-1]
        fib_levels = calculate_fibonacci_levels(df)
        tp_levels = calculate_fib_take_profits(exit_price, fib_levels, "Short")
        stop_loss = calculate_fib_stop_loss(exit_price, fib_levels, "Short")
        leverage = calculate_leverage(df['ADX'].iloc[-1], df['ATR'].iloc[-1], calculate_trend_strength(df))
        
        logging.info(f"Short position for {symbol} with leverage {leverage}, Entry at {exit_price}, Take profits at {tp_levels}, Stop-loss at {stop_loss}")
        return {
            'Symbol': symbol,
            'Signal': 'Short',
            'Entry': exit_price,
            'Leverage': leverage,
            'TakeProfits': tp_levels,
            'StopLoss': stop_loss
        }

    return {'Symbol': symbol, 'Signal': 'Hold', 'Leverage': 1}

async def analyze_1h(df, symbol):
    # Calculate indicators
    upper_bb, middle_bb, lower_bb = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df['Bollinger_upper'] = upper_bb
    df['Bollinger_middle'] = middle_bb
    df['Bollinger_lower'] = lower_bb
    
    # Stochastic Oscillator
    df['Stoch_K'], df['Stoch_D'] = talib.STOCH(df['high'], df['low'], df['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    
    # RSI
    df['RSI'] = talib.RSI(df['close'], timeperiod=14)
    
    # Calculate OBV
    df['OBV'] = talib.OBV(df['close'], df['volume'])
    
    # ADX
    df['ADX'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
    
    # ATR
    df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)
    
    # MACD
    df['MACD'], df['MACD_signal'], _ = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    
    adx_value = df['ADX'].iloc[-1]
    atr_value = df['ATR'].iloc[-1]
    trend_strength = calculate_trend_strength(df)
    fib_levels = calculate_fibonacci_levels(df)

    # Calculate Ichimoku
    tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span = talib.ICHIMOKU(df['high'], df['low'], df['close'])
    
    # Use the most recent values
    current_close = df['close'].iloc[-1]
    previous_close = df['close'].iloc[-2]
    upper_bb = df['Bollinger_upper'].iloc[-1]
    lower_bb = df['Bollinger_lower'].iloc[-1]
    tenkan_sen = tenkan_sen.iloc[-1]
    kijun_sen = kijun_sen.iloc[-1]
    senkou_span_a = senkou_span_a.iloc[-26]  # 26 periods ahead
    senkou_span_b = senkou_span_b.iloc[-26]  # 26 periods ahead
    
    # Fine-tune leverage
    leverage = calculate_leverage(adx_value, atr_value, trend_strength)

    # Entry logic - Price Action
    price_above_bb = current_close > upper_bb
    price_above_cloud = current_close > senkou_span_a and current_close > senkou_span_b
    tenkan_kijun_cross = (tenkan_sen > kijun_sen) and (df['tenkan_sen'].iloc[-2] <= df['kijun_sen'].iloc[-2])
    stoch_cross = (df['Stoch_K'].iloc[-1] > df['Stoch_D'].iloc[-1]) and (df['Stoch_K'].iloc[-2] <= df['Stoch_D'].iloc[-2])
    obv_uptrend = df['OBV'].iloc[-1] > df['OBV'].iloc[-5]  # Comparing with 5 periods ago, adjust as needed

    if price_above_bb and price_above_cloud and tenkan_kijun_cross and stoch_cross and obv_uptrend:
        entry_price = current_close
        tp_levels = calculate_fib_take_profits(entry_price, fib_levels, "Long")
        stop_loss = calculate_fib_stop_loss(entry_price, fib_levels, "Long")
        
        logging.info(f"Long position for {symbol} with leverage {leverage}, Entry at {entry_price}, Take profits at {tp_levels}, Stop-loss at {stop_loss}")
        return {
            'Symbol': symbol,
            'Signal': 'Long',
            'Entry': entry_price,
            'Leverage': leverage,
            'TakeProfits': tp_levels,
            'StopLoss': stop_loss
        }

    # Exit logic
    elif current_close < lower_bb or (df['MACD'].iloc[-1] < df['MACD_signal'].iloc[-1]):
        exit_price = current_close
        tp_levels = calculate_fib_take_profits(exit_price, fib_levels, "Short")
        stop_loss = calculate_fib_stop_loss(exit_price, fib_levels, "Short")
        
        logging.info(f"Short position for {symbol} with leverage {leverage}, Entry at {exit_price}, Take profits at {tp_levels}, Stop-loss at {stop_loss}")
        return {
            'Symbol': symbol,
            'Signal': 'Short',
            'Entry': exit_price,
            'Leverage': leverage,
            'TakeProfits': tp_levels,
            'StopLoss': stop_loss
        }

    return {'Symbol': symbol, 'Signal': 'Hold', 'Leverage': 1}

async def analyze_15m(df, symbol):
    # Calculate indicators
    df["fast_ema"] = talib.EMA(df['close'], timeperiod=12)
    df["slow_ema"] = talib.EMA(df['close'], timeperiod=26)
    df["macd"], df["macd_signal"], _ = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df["macd_diff"] = df["macd"] - df["macd_signal"]    
    
    # Session VWAP: Calculated from the start of the trading session
    df['vwap'] = talib.VWAP(df['high'], df['low'], df['close'], df['volume'])
    
    # RSI
    df['RSI'] = talib.RSI(df['close'], timeperiod=14)
    overbought_rsi = 70
    oversold_rsi = 30
    
    # Current volume
    current_volume = df['volume'].iloc[-1]
    volume_ma = df['volume'].rolling(window=20).mean().iloc[-1]

    # Entry Criteria (Long Position):
    if (df["fast_ema"].iloc[-1] > df["slow_ema"].iloc[-1] and
        df["fast_ema"].iloc[-2] <= df["slow_ema"].iloc[-2] and
        df["macd_diff"].iloc[-1] > 0 and
        df["RSI"].iloc[-1] > oversold_rsi and
        current_volume > volume_ma and
        df['close'].iloc[-1] > df['vwap'].iloc[-1]):
        
        entry_price = df['close'].iloc[-1]
        fib_levels = calculate_fibonacci_levels(df)
        tp_levels = calculate_fib_take_profits(entry_price, fib_levels, "Long")
        stop_loss = calculate_fib_stop_loss(entry_price, fib_levels, "Long")
        leverage = calculate_leverage(df['ADX'].iloc[-1], df['ATR'].iloc[-1], calculate_trend_strength(df))
        
        logging.info(f"Long position for {symbol} with leverage {leverage}, Entry at {entry_price}, Take profits at {tp_levels}, Stop-loss at {stop_loss}")
        return {
            'Symbol': symbol,
            'Signal': 'Long',
            'Entry': entry_price,
            'Leverage': leverage,
            'TakeProfits': tp_levels,
            'StopLoss': stop_loss
        }

    # Exit Criteria (Short Position):
    elif (df["fast_ema"].iloc[-1] < df["slow_ema"].iloc[-1] and
          df["fast_ema"].iloc[-2] >= df["slow_ema"].iloc[-2] and
          df["macd"].iloc[-1] < df["macd_signal"].iloc[-1] and
          df["RSI"].iloc[-1] < overbought_rsi):
        
        exit_price = df['close'].iloc[-1]
        fib_levels = calculate_fibonacci_levels(df)
        tp_levels = calculate_fib_take_profits(exit_price, fib_levels, "Short")
        stop_loss = calculate_fib_stop_loss(exit_price, fib_levels, "Short")
        leverage = calculate_leverage(df['ADX'].iloc[-1], df['ATR'].iloc[-1], calculate_trend_strength(df))
        
        logging.info(f"Short position for {symbol} with leverage {leverage}, Entry at {exit_price}, Take profits at {tp_levels}, Stop-loss at {stop_loss}")
        return {
            'Symbol': symbol,
            'Signal': 'Short',
            'Entry': exit_price,
            'Leverage': leverage,
            'TakeProfits': tp_levels,
            'StopLoss': stop_loss
        }

    return {'Symbol': symbol, 'Signal': 'Hold', 'Leverage': 1}

async def analyze_all_timeframes(symbol):
    data_fetcher = DataFetcher()

    async with ClientSession() as session:
        # Fetch data for all timeframes
        data_weekly = await data_fetcher.get_historical_data(session, symbol, 'week', 52, 1)
        data_daily = await data_fetcher.get_historical_data(session, symbol, 'day', 365, 1)
        data_4h = await data_fetcher.get_historical_data(session, symbol, 'hour', 168, 4)
        data_1h = await data_fetcher.get_historical_data(session, symbol, 'hour', 24, 1)
        data_15m = await data_fetcher.get_historical_data(session, symbol, 'minute', 96, 15)

    long_term_trend = await analyze_weekly(data_weekly)
    daily_signal = await analyze_daily(data_daily)
    signal_4h = await analyze_4h(data_4h, symbol)
    signal_1h = await analyze_1h(data_1h, symbol)
    signal_15m = await analyze_15m(data_15m, symbol)

    if long_term_trend == 'Bullish' and daily_signal == 'Breakout':
        if signal_4h['Signal'] == 'Long' and signal_1h['Signal'] == 'Long' and signal_15m['Signal'] == 'Long':
            return {
                'Symbol': symbol,
                'Signal': 'Strong Long',
                'Confidence': 'Very High',
                'Entry': data_15m['close'].iloc[-1],
                'StopLoss': calculate_stop_loss(data_15m, 'Long'),
                'TakeProfit': calculate_take_profit(data_daily, 'Long')  # Using daily chart for TP
            }
    elif long_term_trend == 'Bearish' and daily_signal == 'Breakdown':
        if signal_4h['Signal'] == 'Short' and signal_1h['Signal'] == 'Short' and signal_15m['Signal'] == 'Short':
            return {
                'Symbol': symbol,
                'Signal': 'Strong Short',
                'Confidence': 'Very High',
                'Entry': data_15m['close'].iloc[-1],
                'StopLoss': calculate_stop_loss(data_15m, 'Short'),
                'TakeProfit': calculate_take_profit(data_daily, 'Short')  # Using daily chart for TP
            }
    
    # Add more conditions for other scenarios
    elif long_term_trend == 'Neutral' and daily_signal == 'Breakout':
        if signal_4h['Signal'] == 'Long' and signal_1h['Signal'] == 'Long':
            return {
                'Symbol': symbol,
                'Signal': 'Moderate Long',
                'Confidence': 'Medium',
                'Entry': data_1h['close'].iloc[-1],
                'StopLoss': calculate_stop_loss(data_1h, 'Long'),
                'TakeProfit': calculate_take_profit(data_4h, 'Long')  # Using 4H chart for TP
            }
    elif long_term_trend == 'Neutral' and daily_signal == 'Breakdown':
        if signal_4h['Signal'] == 'Short' and signal_1h['Signal'] == 'Short':
            return {
                'Symbol': symbol,
                'Signal': 'Moderate Short',
                'Confidence': 'Medium',
                'Entry': data_1h['close'].iloc[-1],
                'StopLoss': calculate_stop_loss(data_1h, 'Short'),
                'TakeProfit': calculate_take_profit(data_4h, 'Short')  # Using 4H chart for TP
            }
    elif long_term_trend == 'Bullish' and daily_signal == 'Range':
        if signal_4h['Signal'] == 'Long' and signal_1h['Signal'] == 'Long':
            return {
                'Symbol': symbol,
                'Signal': 'Weak Long',
                'Confidence': 'Low',
                'Entry': data_1h['close'].iloc[-1],
                'StopLoss': calculate_stop_loss(data_1h, 'Long'),
                'TakeProfit': calculate_take_profit(data_4h, 'Long')  # Using 4H chart for TP
            }
    elif long_term_trend == 'Bearish' and daily_signal == 'Range':
        if signal_4h['Signal'] == 'Short' and signal_1h['Signal'] == 'Short':
            return {
                'Symbol': symbol,
                'Signal': 'Weak Short',
                'Confidence': 'Low',
                'Entry': data_1h['close'].iloc[-1],
                'StopLoss': calculate_stop_loss(data_1h, 'Short'),
                'TakeProfit': calculate_take_profit(data_4h, 'Short')  # Using 4H chart for TP
            }

    return {'Symbol': symbol, 'Signal': 'No Clear Signal', 'Confidence': 'Low'}