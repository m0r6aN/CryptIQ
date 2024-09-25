import os
import ccxt
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests
import sys
from io import StringIO
from datetime import datetime

class BlofimTradingBot:
    def __init__(self, symbols, cryptocompare_api_key, c=14, a=3, h=False):
        self.c = c  # ATR period
        self.a = a  # Multiplier for ATR trailing stop
        self.h = h  # Some boolean flag, define its purpose
        self.exchange = ccxt.blofin({
            'apiKey': os.getenv('BLOFIN_API_KEY'),
            'secret': os.getenv('BLOFIN_SECRET'),
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        self.symbols = symbols
        self.cryptocompare_api_key = os.getenv('CRYPTOCOMPARE_API_KEY')       
        self.leverage = 1.0

    def fetch_cryptocompare_data(self, symbol: str, start_date: str, end_date: str, timeframe: str) -> pd.DataFrame:
        base = symbol
        quote = 'USDT'        

        # Determine the appropriate URL based on the timeframe
        if timeframe == 'day':
            base_url = "https://min-api.cryptocompare.com/data/v2/histoday"
            aggregate = 1
        elif timeframe in ['hour', '4hour', '6hour', '8hour', '12hour']:
            base_url = "https://min-api.cryptocompare.com/data/v2/histohour"
            aggregate = int(timeframe.replace('hour', ''))
        else:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        print(f'Fetching data for {symbol} with {timeframe} timeframe using {base_url}')
        
        start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
        
        all_data = []
        current_timestamp = end_timestamp

        while current_timestamp > start_timestamp:
            params = {
                'fsym': base,  # Base symbol (e.g., BTC)
                'tsym': quote,  # Quote symbol (e.g., USDT)
                'limit': 2000,  # Max data points to retrieve
                'aggregate': aggregate,  # Aggregation period (e.g., 4-hour candles)
                'toTs': current_timestamp,  # Get data up to this specific timestamp
                'api_key': self.cryptocompare_api_key 
            }

            response = requests.get(base_url, params=params)
            data = response.json()

            if data['Response'] == 'Success':
                df = pd.DataFrame(data['Data']['Data'])
                all_data.append(df)

                # Move the timestamp back to the oldest point from the last batch
                current_timestamp = df['time'].min() - 1
            else:
                print(f"Error fetching data: {data['Message']}")
                break

        if not all_data:
            return pd.DataFrame()

        # Concatenate all the fetched data into a single dataframe
        df = pd.concat(all_data, ignore_index=True)
        
        # Convert timestamps to datetime and filter by start_date and end_date
        df['timestamp'] = pd.to_datetime(df['time'], unit='s')
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)
        df = df[(df['timestamp'] >= start_datetime) & (df['timestamp'] <= end_datetime)]

        # Rename columns appropriately
        df = df.rename(columns={
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volumefrom': 'volume',
            'volumeto': 'quote_volume'
        })
        
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]


    def fetch_trading_signals(self, symbol: str) -> Dict:
        url = f"https://min-api.cryptocompare.com/data/tradingsignals/intotheblock/latest"
        params = {
            'fsym': symbol,
            'api_key': self.cryptocompare_api_key
        }

        print(f'Fetching trading signals for {symbol} using {url}')
        
        response = requests.get(url, params=params)
        data = response.json()

        if data.get('Response') == 'Success' and 'Data' in data:
            # Extract the signals from the response
            signals = data['Data']
            
            # Process the signals into a more usable format
            processed_signals = {}

            for key, signal in signals.items():
                if isinstance(signal, dict):
                    sentiment = signal.get('sentiment')
                    score = signal.get('score', 0)
                    bullish_threshold = signal.get('score_threshold_bullish', 0.75)
                    bearish_threshold = signal.get('score_threshold_bearish', 0.25)
                    
                    # Determine the signal strength and whether it's bullish or bearish
                    signal_strength = 'neutral'
                    
                    if sentiment == 'bullish' and score >= bullish_threshold:
                        signal_strength = 'bullish'
                    elif sentiment == 'bearish' and score >= bearish_threshold:
                        signal_strength = 'bearish'
                    
                    processed_signals[key] = {
                        'category': signal.get('category', 'unknown'),
                        'sentiment': sentiment,
                        'score': score,
                        'bullish_threshold': bullish_threshold,
                        'bearish_threshold': bearish_threshold,
                        'signal_strength': signal_strength
                    }

            return processed_signals
        else:
            print(f"Error fetching trading signals: {data.get('Message', 'Unknown error')}")
            return {}

    def calculate_atr(self, df: pd.DataFrame) -> pd.Series:
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(self.c).mean()

    def calculate_atr_trailing_stop(self, df: pd.DataFrame, atr: pd.Series) -> pd.Series:
        src = df['close'] if not self.h else df['close']
        n_loss = self.a * atr
        atr_trailing_stop = pd.Series(index=df.index)
        for i in range(len(df)):
            if i == 0:
                atr_trailing_stop.iloc[i] = src.iloc[i] - n_loss.iloc[i]
            else:
                prev_value = atr_trailing_stop.iloc[i-1]
                if src.iloc[i] > prev_value and src.iloc[i-1] > prev_value:
                    atr_trailing_stop.iloc[i] = max(prev_value, src.iloc[i] - n_loss.iloc[i])
                elif src.iloc[i] < prev_value and src.iloc[i-1] < prev_value:
                    atr_trailing_stop.iloc[i] = min(prev_value, src.iloc[i] + n_loss.iloc[i])
                else:
                    atr_trailing_stop.iloc[i] = src.iloc[i] - n_loss.iloc[i] if src.iloc[i] > prev_value else src.iloc[i] + n_loss.iloc[i]
        return atr_trailing_stop

    def backtest(self, symbol: str, start_date: str, end_date: str, timeframe: str, initial_balance: float = 100000) -> Optional[Dict]:
        trades = [] # Call to Backtester class
        
        return self.calculate_metrics(trades, initial_balance)

    def calculate_metrics(self, trades: List[Dict], initial_balance: float) -> Dict:
        if not trades:
            return {
                'final_balance': initial_balance,
                'total_return': 0,
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'average_win': 0,
                'average_loss': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0,
                'trades': []
            }
        
        df = pd.DataFrame(trades)
        df['cumulative_profit'] = df['profit'].cumsum()
        df['cumulative_balance'] = initial_balance + df['cumulative_profit']
        df['drawdown'] = df['cumulative_balance'].cummax() - df['cumulative_balance']
        df['drawdown_pct'] = df['drawdown'] / df['cumulative_balance'].cummax()

        winning_trades = df[df['profit'] > 0]
        losing_trades = df[df['profit'] < 0]

        results = {
            'final_balance': df['balance'].iloc[-1] if not df.empty else initial_balance,
            'total_return': ((df['balance'].iloc[-1] if not df.empty else initial_balance) - initial_balance) / initial_balance * 100,
            'total_trades': len(df),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': len(winning_trades) / len(df) * 100 if len(df) > 0 else 0,
            'average_win': winning_trades['profit'].mean() if len(winning_trades) > 0 else 0,
            'average_loss': losing_trades['profit'].mean() if len(losing_trades) > 0 else 0,
            'profit_factor': abs(winning_trades['profit'].sum() / losing_trades['profit'].sum()) if len(losing_trades) > 0 else float('inf'),
            'max_drawdown': df['drawdown_pct'].max() * 100,
            'sharpe_ratio': self.calculate_sharpe_ratio(df['profit']),
            'trades': trades
        }
        return results

    def calculate_sharpe_ratio(self, profits, initial_balance, risk_free_rate=0.01):
        returns = profits / initial_balance
  
        if len(returns) == 0:
            return 0
        returns_series = pd.Series(returns)
        excess_returns = returns_series - (risk_free_rate / 252)  # Assuming daily returns and annualized risk-free rate
        return np.sqrt(252) * excess_returns.mean() / excess_returns.std() if excess_returns.std() != 0 else 0

    def print_backtest_results(self, results: Optional[Dict], symbol: str):
        if results is None:
            print(f"No backtest results available for {symbol}.")
            return

        print(f"\nBacktest Results for {symbol}")
        print(f"Final Balance: ${results['final_balance']:.2f}")
        print(f"Total Return: {results['total_return']:.2f}%")
        print(f"Total Trades: {results['total_trades']}")
        print(f"Winning Trades: {results['winning_trades']}")
        print(f"Losing Trades: {results['losing_trades']}")
        print(f"Win Rate: {results['win_rate']:.2f}%")
        print(f"Average Winning Trade: ${results['average_win']:.2f}")
        print(f"Average Losing Trade: ${results['average_loss']:.2f}")
        print(f"Profit Factor: {results['profit_factor']:.2f}")
        print(f"Maximum Drawdown: {results['max_drawdown']:.2f}%")
        print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")

        if results['trades']:
            print("\nTrade History:")
            trades_df = pd.DataFrame(results['trades'])
            print(trades_df)
        else:
            print("\nNo trades were executed during the backtest period.")

if __name__ == "__main__":
    API_KEY = 'f2be02aeaece4cbf8bd2fadee5e4654b'
    SECRET = 'e892ca4192854dfa82e4cb6fb6d77cee'
    #SYMBOLS = ['BTC', 'ETH', 'XRP', 'FIL', 'AR', 'SOL', 'SUI', 'THETA'] 
    SYMBOLS = ['BTC'] 
    TIMEFRAMES = ['hour', '4hour', '6hour', '8hour', '12hour', 'day']
    CRYPTOCOMPARE_API_KEY = '91f6b7467a315915332780b1fab004d8a7490650d5b38d350b494f92a4bfd6c4'

    bot = BlofimTradingBot(API_KEY, SECRET, SYMBOLS, CRYPTOCOMPARE_API_KEY)
    
    # Run backtest
    start_date = '2023-01-01'
    end_date = '2024-09-30'

    # Create a file to save the results
    for symbol in SYMBOLS:
        for timeframe in TIMEFRAMES:
            with open(f'{symbol}_{timeframe}_results.txt', 'w') as f:
                # Redirect stdout to capture print output
                old_stdout = sys.stdout
                sys.stdout = StringIO()

                print(f"\nRunning backtest for {symbol} with {timeframe} timeframe")
                backtest_results = bot.backtest(symbol, start_date, end_date, timeframe)
                bot.print_backtest_results(backtest_results, symbol)

                # Get the captured output and write to file
                output = sys.stdout.getvalue()
                f.write(output)

                # Restore stdout
                sys.stdout = old_stdout

    print("Backtest results have been saved to individual files for each symbol and timeframe")