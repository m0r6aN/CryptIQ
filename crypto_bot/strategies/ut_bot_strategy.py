import ccxt
import pandas as pd
import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta
import yfinance as yf

class BlofimTradingBot:
    def __init__(self, api_key: str, secret: str, symbols: List[str], timeframe: str = '1h',
                 a: float = 1.0, c: int = 10, h: bool = False, leverage: float = 1.0):
        self.exchange = ccxt.blofin({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        self.symbols = symbols
        self.timeframe = timeframe
        self.a = a
        self.c = c
        self.h = h
        self.leverage = leverage

    def fetch_yahoo_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        # Convert CCXT symbol format to Yahoo Finance format
        yf_symbol = symbol.replace('/', '-')
        df = yf.download(yf_symbol, start=start_date, end=end_date, interval="1h")
        df.reset_index(inplace=True)
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
        return df

    def calculate_atr(self, df: pd.DataFrame) -> pd.Series:
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(self.c).mean()

    def calculate_atr_trailing_stop(self, df: pd.DataFrame, atr: pd.Series) -> pd.Series:
        src = df['close'] if not self.h else df['close']  # We don't have Heikin Ashi in this implementation
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

    def backtest(self, symbol: str, start_date: str, end_date: str, initial_balance: float = 100000):
        df = self.fetch_yahoo_data(symbol, start_date, end_date)
        atr = self.calculate_atr(df)
        atr_trailing_stop = self.calculate_atr_trailing_stop(df, atr)

        balance = initial_balance
        position = {'side': None, 'amount': 0, 'entry_price': 0}
        trades = []
        
        for i in range(1, len(df)):
            current_price = df['close'].iloc[i]
            prev_price = df['close'].iloc[i-1]
            current_stop = atr_trailing_stop.iloc[i]
            prev_stop = atr_trailing_stop.iloc[i-1]

            if position['side'] is None:
                if prev_price <= prev_stop and current_price > current_stop:
                    # Buy signal
                    position = {'side': 'long', 'amount': balance * self.leverage / current_price, 'entry_price': current_price}
                    trades.append({
                        'timestamp': df['timestamp'].iloc[i],
                        'type': 'buy',
                        'price': current_price,
                        'amount': position['amount'],
                        'balance': balance
                    })
                elif prev_price >= prev_stop and current_price < current_stop:
                    # Sell signal
                    position = {'side': 'short', 'amount': balance * self.leverage / current_price, 'entry_price': current_price}
                    trades.append({
                        'timestamp': df['timestamp'].iloc[i],
                        'type': 'sell',
                        'price': current_price,
                        'amount': position['amount'],
                        'balance': balance
                    })
            elif position['side'] == 'long' and current_price < current_stop:
                # Close long position
                profit = (current_price - position['entry_price']) * position['amount']
                balance += profit
                trades.append({
                    'timestamp': df['timestamp'].iloc[i],
                    'type': 'sell',
                    'price': current_price,
                    'amount': position['amount'],
                    'profit': profit,
                    'balance': balance
                })
                position = {'side': None, 'amount': 0, 'entry_price': 0}
            elif position['side'] == 'short' and current_price > current_stop:
                # Close short position
                profit = (position['entry_price'] - current_price) * position['amount']
                balance += profit
                trades.append({
                    'timestamp': df['timestamp'].iloc[i],
                    'type': 'buy',
                    'price': current_price,
                    'amount': position['amount'],
                    'profit': profit,
                    'balance': balance
                })
                position = {'side': None, 'amount': 0, 'entry_price': 0}

        # Close any open position at the end of the backtest
        if position['side'] is not None:
            final_price = df['close'].iloc[-1]
            if position['side'] == 'long':
                profit = (final_price - position['entry_price']) * position['amount']
            else:
                profit = (position['entry_price'] - final_price) * position['amount']
            balance += profit
            trades.append({
                'timestamp': df['timestamp'].iloc[-1],
                'type': 'close',
                'price': final_price,
                'amount': position['amount'],
                'profit': profit,
                'balance': balance
            })

        return self.calculate_metrics(trades, initial_balance)

    def calculate_metrics(self, trades: List[Dict], initial_balance: float) -> Dict:
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

    def calculate_sharpe_ratio(self, returns, risk_free_rate=0.01):
        if len(returns) == 0:
            return 0
        returns_series = pd.Series(returns)
        excess_returns = returns_series - (risk_free_rate / 252)  # Assuming daily returns and annualized risk-free rate
        return np.sqrt(252) * excess_returns.mean() / excess_returns.std() if excess_returns.std() != 0 else 0

    def print_backtest_results(self, results: Dict):
        print("\nBacktest Results")
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

        print("\nTrade History:")
        trades_df = pd.DataFrame(results['trades'])
        print(trades_df)

if __name__ == "__main__":
    if __name__ == "__main__":
        API_KEY = 'f2be02aeaece4cbf8bd2fadee5e4654b'
        SECRET = 'e892ca4192854dfa82e4cb6fb6d77cee'
        SYMBOLS = ['BTC-USDT', 'ETH-USDT', 'XRP-USDT','FIL-USDT', 'AR-USDT', 'SOL-USDT','SUI-USDT', 'THETA-USDT','SUI-USDT'] 
    
        bot = BlofimTradingBot(API_KEY, SECRET, SYMBOLS)
        
        # Run backtest
        start_date = '2023-01-01'
        end_date = '2024-09-31'
        backtest_results = bot.backtest(SYMBOLS[0], start_date, end_date)
        bot.print_backtest_results(backtest_results)
        
        # Uncomment the following line to run the live trading bot
        # bot.run()